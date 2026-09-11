from io import StringIO
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from apps.content.models import Article, ContentCategory

User = get_user_model()


class LoadP13AEditorialContentCommandTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="jorgecyberpunktcg",
            email="jorgecyberpunktcg@gmail.com",
            password="testpassword123",
        )

    def test_first_execution_creates_categories_and_articles(self):
        out = StringIO()
        call_command("load_p1_3a_editorial_content", stdout=out)

        self.assertEqual(ContentCategory.objects.count(), 2)
        self.assertEqual(Article.objects.count(), 3)
        self.assertEqual(Article.objects.filter(article_type=Article.ArticleType.GUIDE).count(), 2)
        self.assertEqual(Article.objects.filter(article_type=Article.ArticleType.STRATEGY).count(), 1)
        self.assertIn("Category 'plataforma': CREATE", out.getvalue())
        self.assertIn("Category 'construccion-de-mazos': CREATE", out.getvalue())
        self.assertIn("Article 'bienvenido-a-jorgecyberpunktcg': CREATE", out.getvalue())
        self.assertIn("Article 'como-usar-tu-cyberdeck': CREATE", out.getvalue())
        self.assertIn("Article 'antes-de-construir-define-el-proposito-de-tu-mazo': CREATE", out.getvalue())

    def test_second_execution_is_idempotent_and_outputs_exists(self):
        call_command("load_p1_3a_editorial_content")

        out = StringIO()
        call_command("load_p1_3a_editorial_content", stdout=out)

        self.assertEqual(ContentCategory.objects.count(), 2)
        self.assertEqual(Article.objects.count(), 3)
        self.assertIn("Category 'plataforma': EXISTS", out.getvalue())
        self.assertIn("Category 'construccion-de-mazos': EXISTS", out.getvalue())
        self.assertIn("Article 'bienvenido-a-jorgecyberpunktcg': EXISTS", out.getvalue())
        self.assertIn("Article 'como-usar-tu-cyberdeck': EXISTS", out.getvalue())
        self.assertIn("Article 'antes-de-construir-define-el-proposito-de-tu-mazo': EXISTS", out.getvalue())

    def test_dry_run_does_not_persist_records(self):
        out = StringIO()
        call_command("load_p1_3a_editorial_content", dry_run=True, stdout=out)

        self.assertEqual(ContentCategory.objects.count(), 0)
        self.assertEqual(Article.objects.count(), 0)
        self.assertIn("DRY RUN SUCCESSFUL: 0 database changes persisted.", out.getvalue())

    def test_missing_author_aborts_command(self):
        self.author.delete()
        err = StringIO()
        with self.assertRaises(CommandError) as ctx:
            call_command("load_p1_3a_editorial_content", stderr=err)
        self.assertIn("Author user 'jorgecyberpunktcg' does not exist", str(ctx.exception))
        self.assertEqual(ContentCategory.objects.count(), 0)
        self.assertEqual(Article.objects.count(), 0)

    def test_category_conflict_causes_command_error_and_rollback(self):
        ContentCategory.objects.create(
            slug="plataforma",
            name="Nombre Diferente Conflicto",
            description="Descripcion diferente",
        )
        err = StringIO()
        with self.assertRaises(CommandError) as ctx:
            call_command("load_p1_3a_editorial_content", stderr=err)

        self.assertIn("Conflict detected", str(ctx.exception))
        self.assertEqual(ContentCategory.objects.count(), 1)
        self.assertEqual(Article.objects.count(), 0)

    def test_article_conflict_causes_command_error_and_rollback(self):
        cat = ContentCategory.objects.create(
            slug="plataforma",
            name="Plataforma",
            description="Guías sobre el uso, funcionalidades y visión del proyecto JorgeCyberpunkTCG.",
        )
        Article.objects.create(
            slug="bienvenido-a-jorgecyberpunktcg",
            title="Titulo Conflicto Diferente",
            article_type=Article.ArticleType.GUIDE,
            category=cat,
            author=self.author,
            summary="Resumen conflicto",
            body="Cuerpo conflicto",
            status=Article.Status.PUBLISHED,
        )

        err = StringIO()
        with self.assertRaises(CommandError) as ctx:
            call_command("load_p1_3a_editorial_content", stderr=err)

        self.assertIn("Conflict detected", str(ctx.exception))
        self.assertEqual(ContentCategory.objects.count(), 1)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.first().title, "Titulo Conflicto Diferente")

    def test_does_not_modify_other_unrelated_records(self):
        unrelated_cat = ContentCategory.objects.create(
            slug="otra-categoria",
            name="Otra Categoria",
            description="Otra desc",
        )
        unrelated_art = Article.objects.create(
            slug="otro-articulo",
            title="Otro Articulo",
            article_type=Article.ArticleType.GUIDE,
            category=unrelated_cat,
            author=self.author,
            summary="Otro resumen",
            body="Otro cuerpo",
            status=Article.Status.PUBLISHED,
        )

        call_command("load_p1_3a_editorial_content")

        self.assertEqual(ContentCategory.objects.count(), 3)
        self.assertEqual(Article.objects.count(), 4)
        unrelated_art.refresh_from_db()
        self.assertEqual(unrelated_art.title, "Otro Articulo")

    def test_created_articles_are_publicly_visible(self):
        call_command("load_p1_3a_editorial_content")

        public_articles = Article.objects.publicly_visible()
        self.assertEqual(public_articles.count(), 3)
        self.assertEqual(public_articles.filter(article_type=Article.ArticleType.GUIDE).count(), 2)
        self.assertEqual(public_articles.filter(article_type=Article.ArticleType.STRATEGY).count(), 1)
