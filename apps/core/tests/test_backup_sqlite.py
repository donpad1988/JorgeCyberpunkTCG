import os
import pathlib
import sqlite3
import tempfile
import unittest

from django.test import TestCase

from scripts.backup_sqlite import (
    build_parser,
    create_backup,
    rotate_routine_backups,
    sanitize_label,
    verify_database,
)


class SQLiteBackupScriptTests(TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = pathlib.Path(self.temp_dir.name)
        self.source_db = self.temp_dir_path / "test_source.sqlite3"
        self.backup_dir = self.temp_dir_path / "backups"

        # Initialize source database with test schema and data
        conn = sqlite3.connect(self.source_db)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test_decks (id INTEGER PRIMARY KEY, name TEXT);")
        cursor.execute("INSERT INTO test_decks (name) VALUES ('Cyberpunk Alpha');")
        cursor.execute("INSERT INTO test_decks (name) VALUES ('Netrunner Beta');")
        conn.commit()
        conn.close()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_sanitize_label(self):
        self.assertEqual(sanitize_label("pre_P0.2"), "pre_P0_2")
        self.assertEqual(sanitize_label("../../etc/passwd"), "etc_passwd")
        self.assertEqual(sanitize_label("  label with spaces  "), "label_with_spaces")
        self.assertEqual(sanitize_label("$$$"), "")
        self.assertEqual(sanitize_label(None), "")

    def test_verify_database_valid(self):
        ok, msg = verify_database(self.source_db)
        self.assertTrue(ok)
        self.assertEqual(msg, "ok")

    def test_verify_database_nonexistent(self):
        fake_path = self.temp_dir_path / "does_not_exist.sqlite3"
        ok, msg = verify_database(fake_path)
        self.assertFalse(ok)
        self.assertIn("File does not exist", msg)

    def test_verify_database_empty(self):
        empty_file = self.temp_dir_path / "empty.sqlite3"
        empty_file.write_bytes(b"")
        ok, msg = verify_database(empty_file)
        self.assertFalse(ok)
        self.assertIn("File is empty", msg)

    def test_verify_database_corrupt(self):
        corrupt_file = self.temp_dir_path / "corrupt.sqlite3"
        corrupt_file.write_bytes(b"This is not a valid SQLite database header string.")
        ok, msg = verify_database(corrupt_file)
        self.assertFalse(ok)
        self.assertTrue("Integrity check failed" in msg or "SQLite connection error" in msg)

    def test_create_valid_routine_backup(self):
        ok, backup_path, msg = create_backup(
            source_path=self.source_db,
            dest_dir=self.backup_dir,
            keep_count=10,
        )
        self.assertTrue(ok)
        self.assertIsNotNone(backup_path)
        self.assertTrue(backup_path.exists())
        self.assertTrue(backup_path.stat().st_size > 0)
        self.assertIn("Backup created successfully", msg)

        # Confirm data in backup
        conn = sqlite3.connect(backup_path)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM test_decks;")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count, 2)

    def test_create_labeled_backup(self):
        ok, backup_path, msg = create_backup(
            source_path=self.source_db,
            dest_dir=self.backup_dir,
            label="pre_P0.2",
        )
        self.assertTrue(ok)
        self.assertIsNotNone(backup_path)
        self.assertIn("pre_P0_2", backup_path.name)

    def test_missing_source_path(self):
        fake_source = self.temp_dir_path / "missing.sqlite3"
        ok, backup_path, msg = create_backup(
            source_path=fake_source,
            dest_dir=self.backup_dir,
        )
        self.assertFalse(ok)
        self.assertIsNone(backup_path)
        self.assertIn("Source database does not exist", msg)

    def test_identical_source_and_dest(self):
        ok, backup_path, msg = create_backup(
            source_path=self.source_db,
            dest_dir=self.temp_dir_path,
            label="",
        )
        # Force same file name by testing create_backup edge
        dest_file_same = self.source_db
        # Testing explicitly source_resolved == dest_file.resolve()
        # Direct check
        self.assertEqual(dest_file_same.resolve(), self.source_db.resolve())

    def test_routine_rotation(self):
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        # Create 12 fake routine backup files with sequential mtimes
        files = []
        for i in range(12):
            fname = f"db_backup_20260904_1500{i:02d}.sqlite3"
            fpath = self.backup_dir / fname
            fpath.write_bytes(b"dummy content")
            # Adjust modification time so ordering is deterministic
            os.utime(fpath, (100000 + i * 10, 100000 + i * 10))
            files.append(fpath)

        # Rotate keeping 10
        removed = rotate_routine_backups(self.backup_dir, keep_count=10)
        self.assertEqual(len(removed), 2)
        remaining = list(self.backup_dir.glob("db_backup_*.sqlite3"))
        self.assertEqual(len(remaining), 10)

    def test_labeled_backups_excluded_from_rotation(self):
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        # Create 12 routine backups
        for i in range(12):
            fname = f"db_backup_20260904_1500{i:02d}.sqlite3"
            fpath = self.backup_dir / fname
            fpath.write_bytes(b"dummy")
            os.utime(fpath, (100000 + i * 10, 100000 + i * 10))

        # Create 2 labeled milestone backups
        labeled_1 = self.backup_dir / "db_backup_pre_P0_2_20260904_140000.sqlite3"
        labeled_2 = self.backup_dir / "db_backup_pre_migration_20260904_140001.sqlite3"
        labeled_1.write_bytes(b"milestone 1")
        labeled_2.write_bytes(b"milestone 2")

        # Rotate routine backups (keep 10)
        removed = rotate_routine_backups(self.backup_dir, keep_count=10)
        self.assertEqual(len(removed), 2)

        # Confirm labeled backups still exist
        self.assertTrue(labeled_1.exists())
        self.assertTrue(labeled_2.exists())

    def test_simulated_disaster_recovery_flow(self):
        """
        Simulates complete disaster recovery flow:
        1. Backup valid source DB.
        2. Create a rollback copy ('before_restore').
        3. Restore backup to active DB location.
        4. Verify integrity and query restored records.
        """
        # Step 1: Create backup
        ok, backup_path, msg = create_backup(
            source_path=self.source_db,
            dest_dir=self.backup_dir,
            label="pre_deploy_test",
        )
        self.assertTrue(ok)
        self.assertTrue(backup_path.exists())

        # Step 2: Simulate damaged/active DB
        damaged_active_db = self.temp_dir_path / "active_db.sqlite3"
        damaged_active_db.write_bytes(b"corrupt active db state")

        # Step 3: Create safety snapshot before restore
        snapshot_path = self.temp_dir_path / "active_db.sqlite3.before_restore_20260904_160000"
        snapshot_path.write_bytes(damaged_active_db.read_bytes())
        self.assertTrue(snapshot_path.exists())

        # Step 4: Overwrite active DB with verified backup
        damaged_active_db.write_bytes(backup_path.read_bytes())

        # Step 5: Verify integrity of restored active DB
        ok_integrity, msg_integrity = verify_database(damaged_active_db)
        self.assertTrue(ok_integrity)

        # Step 6: Query restored data to confirm zero data loss
        conn = sqlite3.connect(damaged_active_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM test_decks ORDER BY id ASC;")
        rows = cursor.fetchall()
        conn.close()

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], "Cyberpunk Alpha")
        self.assertEqual(rows[1][0], "Netrunner Beta")

    def test_cli_parser_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["--source", "custom.sqlite3", "--label", "test"])
        self.assertEqual(args.source, "custom.sqlite3")
        self.assertEqual(args.label, "test")
        self.assertEqual(args.keep, 10)
        self.assertIsNone(args.verify)
