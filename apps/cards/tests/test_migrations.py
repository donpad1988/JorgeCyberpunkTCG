from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class CardPrintingDataMigrationTests(TransactionTestCase):
    reset_sequences = True

    def migration_targets(self, cards_migration):
        executor = MigrationExecutor(connection)
        return [
            node for node in executor.loader.graph.leaf_nodes() if node[0] != "cards"
        ] + [("cards", cards_migration)]

    def setUp(self):
        executor = MigrationExecutor(connection)
        executor.migrate(self.migration_targets("0001_initial"))
        old_apps = executor.loader.project_state(self.migration_targets("0001_initial")).apps
        OldSet = old_apps.get_model("cards", "Set")
        OldCard = old_apps.get_model("cards", "Card")
        card_set = OldSet.objects.create(
            name="Welcome to Night City — Retail",
            slug="welcome-to-night-city-retail",
        )
        self.old_card = OldCard.objects.create(
            name="Migration Card",
            slug="migration-card",
            set=card_set,
            collector_number="078",
            cost=3,
            ram=2,
            power=2,
            card_type="UNIT",
            status="PUBLISHED",
            rules_text="Identity data stays on Card.",
            source_name="Official source",
            source_url="https://example.com/migration-card",
            verification_notes="Verified manually",
        )
        executor = MigrationExecutor(connection)
        executor.migrate(self.migration_targets("0003_migrate_cards_to_initial_printings"))
        self.apps = executor.loader.project_state(
            self.migration_targets("0003_migrate_cards_to_initial_printings")
        ).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_legacy_card_becomes_one_primary_printing_with_copied_data(self):
        Card = self.apps.get_model("cards", "Card")
        CardPrinting = self.apps.get_model("cards", "CardPrinting")
        card = Card.objects.get(slug="migration-card")
        printing = CardPrinting.objects.get(card_id=card.pk)

        self.assertTrue(printing.is_primary)
        self.assertEqual(card.name, "Migration Card")
        self.assertEqual(card.slug, "migration-card")
        self.assertEqual(card.status, "PUBLISHED")
        self.assertEqual(printing.collector_number, "078")
        self.assertEqual((printing.cost, printing.ram, printing.power), (3, 2, 2))
        self.assertEqual(printing.source_name, "Official source")
        self.assertEqual(printing.source_url, "https://example.com/migration-card")
        self.assertEqual(printing.verification_notes, "Verified manually")
        self.assertEqual(card.rules_text, "Identity data stays on Card.")
