#!/usr/bin/env python3
"""
SQLite Backup & Integrity Verification Tool for JorgeCyberpunkTCG.

Uses Python Standard Library sqlite3.Connection.backup() to create point-in-time,
online transaccional backups without relying on external sqlite3 CLI binaries.

Usage:
    python scripts/backup_sqlite.py --source db.sqlite3 --destination-dir /path/to/backups --label pre_P0.2
    python scripts/backup_sqlite.py --verify /path/to/backups/db_backup_20260904_153000.sqlite3
"""

import argparse
import datetime
import os
import pathlib
import re
import sqlite3
import sys

ROUTINE_BACKUP_PATTERN = re.compile(r"^db_backup_\d{8}_\d{6}\.sqlite3$")
LABELED_BACKUP_PATTERN = re.compile(r"^db_backup_[a-zA-Z0-9_-]+_\d{8}_\d{6}\.sqlite3$")


def sanitize_label(label: str) -> str:
    """Sanitize label input to prevent path traversal and invalid filename characters."""
    if not label:
        return ""
    # Strip whitespace
    cleaned = label.strip()
    # Replace path separators or directory traversal indicators
    cleaned = cleaned.replace("/", "_").replace("\\", "_").replace("..", "_")
    # Replace any character that is not alphanumeric, hyphen, or underscore
    cleaned = re.sub(r"[^a-zA-Z0-9_-]", "_", cleaned)
    # Collapse multiple underscores
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned


def verify_database(file_path: pathlib.Path) -> tuple[bool, str]:
    """
    Verify the integrity of a SQLite database file using PRAGMA integrity_check.
    Does NOT modify the target file.
    """
    resolved_path = file_path.resolve()
    if not resolved_path.exists():
        return False, f"File does not exist: {resolved_path}"
    if not resolved_path.is_file():
        return False, f"Path is not a regular file: {resolved_path}"
    if resolved_path.stat().st_size == 0:
        return False, f"File is empty (0 bytes): {resolved_path}"

    conn = None
    try:
        # Open in read-only mode using URI filename
        conn = sqlite3.connect(f"file:{resolved_path.as_posix()}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()
        if result and result[0] == "ok":
            return True, "ok"
        else:
            err_msg = result[0] if result else "Unknown integrity check failure"
            return False, f"Integrity check failed: {err_msg}"
    except sqlite3.Error as e:
        return False, f"SQLite connection error: {e}"
    finally:
        if conn:
            conn.close()


def rotate_routine_backups(dest_dir: pathlib.Path, keep_count: int) -> list[pathlib.Path]:
    """
    Rotate routine backups in dest_dir, retaining only the keep_count most recent.
    Labeled backups are excluded from rotation and preserved permanently.
    """
    if keep_count < 1 or not dest_dir.exists():
        return []

    routine_backups = []
    for entry in dest_dir.iterdir():
        if entry.is_file() and ROUTINE_BACKUP_PATTERN.match(entry.name):
            routine_backups.append(entry)

    # Sort routine backups by modification time descending (newest first)
    routine_backups.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    removed = []
    if len(routine_backups) > keep_count:
        to_remove = routine_backups[keep_count:]
        for old_backup in to_remove:
            try:
                old_backup.unlink()
                removed.append(old_backup)
            except OSError as e:
                print(f"Warning: Could not remove old backup {old_backup}: {e}", file=sys.stderr)
    return removed


def create_backup(
    source_path: pathlib.Path,
    dest_dir: pathlib.Path,
    label: str | None = None,
    keep_count: int = 10,
) -> tuple[bool, pathlib.Path | None, str]:
    """
    Create a point-in-time online SQLite backup using sqlite3.Connection.backup().
    Verifies integrity post-creation and rotates routine backups if applicable.
    """
    source_resolved = source_path.resolve()
    if not source_resolved.exists():
        return False, None, f"Source database does not exist: {source_resolved}"
    if not source_resolved.is_file():
        return False, None, f"Source path is not a file: {source_resolved}"

    dest_dir_resolved = dest_dir.resolve()
    dest_dir_resolved.mkdir(parents=True, exist_ok=True)

    # Apply POSIX directory permissions (0700) where available
    if os.name != "nt":
        try:
            dest_dir_resolved.chmod(0o700)
        except OSError:
            pass

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_label = sanitize_label(label) if label else ""

    if sanitized_label:
        filename = f"db_backup_{sanitized_label}_{timestamp}.sqlite3"
    else:
        filename = f"db_backup_{timestamp}.sqlite3"

    dest_file = dest_dir_resolved / filename

    if source_resolved == dest_file.resolve():
        return False, None, "Source and destination paths are identical."

    src_conn = None
    dst_conn = None
    try:
        # Open source database read-only
        src_conn = sqlite3.connect(f"file:{source_resolved.as_posix()}?mode=ro", uri=True)
        # Open destination database
        dst_conn = sqlite3.connect(dest_file)

        # Execute online backup
        with dst_conn:
            src_conn.backup(dst_conn)
    except sqlite3.Error as e:
        if dest_file.exists():
            try:
                dest_file.unlink()
            except OSError:
                pass
        return False, None, f"Backup creation failed: {e}"
    finally:
        if dst_conn:
            dst_conn.close()
        if src_conn:
            src_conn.close()

    # Apply POSIX file permissions (0600) where available
    if os.name != "nt":
        try:
            dest_file.chmod(0o600)
        except OSError:
            pass

    # Verify generated backup integrity
    ok, err = verify_database(dest_file)
    if not ok:
        return False, dest_file, f"Backup generated but integrity verification failed: {err}"

    # Perform rotation if this was a routine (unlabeled) backup
    removed_count = 0
    if not sanitized_label:
        removed_files = rotate_routine_backups(dest_dir_resolved, keep_count)
        removed_count = len(removed_files)

    msg = f"Backup created successfully: {dest_file.name} ({dest_file.stat().st_size} bytes)"
    if removed_count > 0:
        msg += f" [Rotated {removed_count} old routine backup(s)]"
    return True, dest_file, msg


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="SQLite Backup & Verification Tool for JorgeCyberpunkTCG"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="db.sqlite3",
        help="Path to source SQLite database file (default: db.sqlite3)",
    )
    parser.add_argument(
        "--destination-dir",
        type=str,
        default="backups",
        help="Directory to store backup files (default: backups)",
    )
    parser.add_argument(
        "--label",
        type=str,
        default=None,
        help="Optional label for milestone/manual backups (e.g. pre_P0.2, pre_migration)",
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=10,
        help="Number of routine backups to retain during rotation (default: 10)",
    )
    parser.add_argument(
        "--verify",
        type=str,
        default=None,
        help="Verify integrity of an existing SQLite backup file without creating a new one",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.verify:
        verify_path = pathlib.Path(args.verify)
        print(f"Verifying database integrity for: {verify_path}")
        ok, msg = verify_database(verify_path)
        if ok:
            print(f"VERIFICATION SUCCESSFUL: {msg}")
            sys.exit(0)
        else:
            print(f"VERIFICATION FAILED: {msg}", file=sys.stderr)
            sys.exit(1)

    source_path = pathlib.Path(args.source)
    dest_dir = pathlib.Path(args.destination_dir)

    print(f"Initiating SQLite backup from '{source_path}' to '{dest_dir}'...")
    ok, backup_path, msg = create_backup(
        source_path=source_path,
        dest_dir=dest_dir,
        label=args.label,
        keep_count=args.keep,
    )

    if ok:
        print(f"SUCCESS: {msg}")
        sys.exit(0)
    else:
        print(f"FAILURE: {msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
