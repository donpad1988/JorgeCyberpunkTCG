from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.content.models import Article, ContentCategory

CANONICAL_CATEGORIES = [
    {
        "slug": "plataforma",
        "name": "Plataforma",
        "description": "Guías sobre el uso, funcionalidades y visión del proyecto JorgeCyberpunkTCG.",
        "is_active": True,
    },
    {
        "slug": "construccion-de-mazos",
        "name": "Construcción de Mazos",
        "description": "Estrategias y conceptos fundamentales para el diseño y construcción de mazos tácticos.",
        "is_active": True,
    },
]

CANONICAL_ARTICLES = [
    {
        "slug": "bienvenido-a-jorgecyberpunktcg",
        "title": "Bienvenido a JorgeCyberpunkTCG",
        "article_type": Article.ArticleType.GUIDE,
        "category_slug": "plataforma",
        "author_username": "jorgecyberpunktcg",
        "summary": (
            "Introducción a la plataforma independiente JorgeCyberpunkTCG: nuestra visión en fase prelaunch, "
            "la estructura del sitio y las herramientas disponibles para el usuario."
        ),
        "body": (
            "Bienvenido a JorgeCyberpunkTCG, una plataforma independiente dedicada al análisis, "
            "la organización de datos y el desarrollo de herramientas conceptuales sobre Cyberpunk TCG. "
            "En este espacio, entusiastas y practicantes de la estrategia disponen de un entorno estructurado "
            "para consultar información, explorar contenidos y profundizar en el entendimiento del juego.\n\n"
            "Naturaleza Independiente y Declaración de Transparencia\n\n"
            "JorgeCyberpunkTCG es un proyecto desarrollado de forma autónoma por la comunidad. "
            "Esta plataforma no es un sitio oficial, ni cuenta con afiliación, patrocinio ni respaldo de CD PROJEKT RED, "
            "WeirdCo ni de ninguna otra entidad titular de derechos comerciales sobre el universo Cyberpunk.\n\n"
            "El propósito central de este portal es ofrecer análisis, catálogo de datos y herramientas "
            "de apoyo técnico respetando los límites de la divulgación independiente.\n\n"
            "Estructura de la Plataforma\n\n"
            "El sitio está organizado en las siguientes secciones accesibles desde el menú de navegación:\n\n"
            "Inicio (Home): Presentación general del proyecto, acceso directo a la información principal "
            "y visión global de la plataforma.\n\n"
            "Guías: Sección de manuales explicativos sobre el funcionamiento del portal y tutoriales de uso "
            "de las herramientas disponibles.\n\n"
            "Estrategias: Artículos conceptuales y metodologías de análisis orientados a la reflexión táctica "
            "y la planificación de mazos.\n\n"
            "Choomdex: Base de datos central donde se catalogan y organizan las cartas verificadas en el sistema.\n\n"
            "Mazos (Biblioteca de Mazos): Sección preparada para la consulta de composiciones tácticas públicas "
            "conforme se incorporen al catálogo.\n\n"
            "DataStream: Espacio reservado para la integración de contenido audiovisual explicativo a medida "
            "que la producción del sitio avance.\n\n"
            "Fase Prelaunch y Crecimiento Progresivo\n\n"
            "JorgeCyberpunkTCG se encuentra en etapa prelaunch. Durante esta fase, el objetivo prioritario "
            "es consolidar una infraestructura técnica estable y mantener la autenticidad del contenido publicado.\n\n"
            "Tanto el catálogo de cartas como las publicaciones editoriales se expanden de manera gradual, "
            "asegurando que la información registrada responda a datos comprobados en la aplicación.\n\n"
            "Te invitamos a recorrer las secciones activas, consultar las cartas en el Choomdex y revisar "
            "nuestros artículos de análisis. La plataforma continuará evolucionando como una herramienta "
            "de consulta clara, estable y accesible."
        ),
        "status": Article.Status.PUBLISHED,
        "published_at_iso": "2026-09-11T18:20:24.548478+00:00",
    },
    {
        "slug": "como-usar-tu-cyberdeck",
        "title": "Cómo usar tu Cyberdeck: Choomdex, cartas y mazos",
        "article_type": Article.ArticleType.GUIDE,
        "category_slug": "plataforma",
        "author_username": "jorgecyberpunktcg",
        "summary": (
            "Manual de uso para las herramientas de JorgeCyberpunkTCG: aprende a consultar el Choomdex, "
            "examina la información de las cartas y gestiona tus mazos."
        ),
        "body": (
            "Las herramientas de JorgeCyberpunkTCG están integradas en un sistema de consulta que permite "
            "analizar cartas registradas y organizar composiciones de mazos. Este manual explica cómo utilizar "
            "las utilidades disponibles en la plataforma.\n\n"
            "El Choomdex: Base de Datos de Cartas\n\n"
            "El Choomdex es el catálogo donde se registran las cartas verificadas en la base de datos de JorgeCyberpunkTCG.\n\n"
            "Al ingresar al Choomdex, el usuario encuentra el listado de cartas disponibles. Cada entrada muestra "
            "la imagen de la carta, su nombre identificativo y sus atributos principales registrados en el sistema.\n\n"
            "Ficha de Carta y Detalles Registrados\n\n"
            "Al seleccionar una carta en el Choomdex, la aplicación despliega la vista detallada. Esta ficha muestra "
            "exclusivamente los datos guardados en la plataforma:\n\n"
            "Nombre oficial de la carta, tipo de carta y categoría dentro de la estructura de datos.\n\n"
            "Atributos impresos y valores de referencia registrados.\n\n"
            "Información sobre la edición o variante de impresión (printing) correspondiente.\n\n"
            "Sistema de Mazos: Biblioteca Pública y Archivo Personal\n\n"
            "La interacción con mazos se divide en dos áreas:\n\n"
            "Biblioteca Pública de Mazos (Tactical Deck Library): Espacio destinado a la consulta de mazos compartidos. "
            "Durante la etapa actual de prelaunch, esta sección muestra su estado inicial a la espera de publicaciones públicas.\n\n"
            "Archivo Personal de Mazos (Tactical Deck File): Área privada donde cada usuario autenticado puede crear, "
            "modificar y guardar sus propios borradores de mazo.\n\n"
            "Autenticación y Funciones Privadas\n\n"
            "La consulta del Choomdex y la lectura de artículos son de acceso libre y no requieren registro. "
            "La creación y gestión de mazos personales en el Archivo Personal requieren iniciar sesión con una cuenta "
            "registrada en la plataforma.\n\n"
            "Alcance de las Herramientas\n\n"
            "Este manual describe el funcionamiento de la aplicación web de JorgeCyberpunkTCG. No constituye ni reemplaza "
            "un reglamento oficial del juego, sino que sirve como guía de uso para la interfaz y las funciones del sitio."
        ),
        "status": Article.Status.PUBLISHED,
        "published_at_iso": "2026-09-11T18:20:24.671265+00:00",
    },
    {
        "slug": "antes-de-construir-define-el-proposito-de-tu-mazo",
        "title": "Antes de construir: define el propósito de tu mazo",
        "article_type": Article.ArticleType.STRATEGY,
        "category_slug": "construccion-de-mazos",
        "author_username": "jorgecyberpunktcg",
        "summary": (
            "Reflexiones sobre planificación de mazos: aprende a establecer un objetivo claro, "
            "evaluar la función de cada carta y revisar decisiones con método."
        ),
        "body": (
            "La planificación de un mazo es un proceso de organización y análisis. Antes de comenzar a seleccionar "
            "cartas en una lista, conviene definir una idea clara sobre la que estructurar la propuesta. Este artículo "
            "presenta reflexiones generales para abordar la construcción de forma metódica.\n\n"
            "Definir el Propósito Central\n\n"
            "Un aspecto relevante al diseñar una lista es responder cuál es su objetivo principal. En lugar de acumular "
            "cartas por preferencia individual, resulta más efectivo contar con un propósito aglutinador.\n\n"
            "Al planificar, es útil considerar preguntas fundamentales:\n\n"
            "¿Cuál es la idea central para alcanzar una situación favorable durante el juego?\n\n"
            "¿De qué manera se coordinan las cartas seleccionadas para respaldar esa idea?\n\n"
            "¿Qué elementos ayudan a mantener el plan en marcha ante posibles dificultades?\n\n"
            "Evaluar la Función de cada Carta\n\n"
            "Cada selección en un mazo debe contar con una justificación clara. Para analizar la lista sin presposiciones "
            "rígidas, se recomienda formular preguntas de evaluación:\n\n"
            "¿Qué aporta esta carta al propósito principal que definiste?\n\n"
            "¿Cumple una función concreta y comprensible dentro del conjunto?\n\n"
            "¿Existen cartas que están ocupando espacio sin una razón clara?\n\n"
            "¿Qué comportamiento observaste al poner a prueba la combinación?\n\n"
            "Probar, Observar y Ajustar\n\n"
            "La planificación inicial ofrece una primera versión, pero la mejora real surge de la observación práctica. "
            "Tras utilizar un mazo en pruebas reales, conviene revisar qué selecciones funcionaron según lo previsto y cuáles "
            "no aportaron el valor esperado.\n\n"
            "Sustituir piezas de forma gradual, reforzando aquellas decisiones que demostraron utilidad, es un procedimiento "
            "aconsejable para afinar cualquier lista.\n\n"
            "Prudencia Analítica en Fase Prelaunch\n\n"
            "En JorgeCyberpunkTCG adoptamos un enfoque de análisis prudente. Durante la fase prelaunch, evitamos ofrecer "
            "conclusiones absolutas sobre listas definitivas o fórmulas garantizadas. La solidez táctica se desarrolla mediante "
            "la comprensión de conceptos generales y la evaluación objetiva de la experiencia práctica."
        ),
        "status": Article.Status.PUBLISHED,
        "published_at_iso": "2026-09-11T18:20:24.815731+00:00",
    },
]


class Command(BaseCommand):
    help = (
        "Loads canonical P1.3A editorial content (2 categories, 3 articles) "
        "deterministically and idempotently."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Perform a dry run without persisting database changes.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        if dry_run:
            self.stdout.write(self.style.WARNING("--- RUNNING IN DRY-RUN MODE ---"))

        User = get_user_model()
        author_username = "jorgecyberpunktcg"
        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            raise CommandError(
                f"Author user '{author_username}' does not exist in the target database. Aborting."
            )

        summary_report = []
        has_conflict = False

        try:
            with transaction.atomic():
                category_map = {}

                # 1. Process Categories
                for cat_data in CANONICAL_CATEGORIES:
                    slug = cat_data["slug"]
                    try:
                        existing = ContentCategory.objects.get(slug=slug)
                        # Check exact match
                        if (
                            existing.name == cat_data["name"]
                            and existing.description == cat_data["description"]
                            and existing.is_active == cat_data["is_active"]
                        ):
                            category_map[slug] = existing
                            summary_report.append(f"Category '{slug}': EXISTS")
                        else:
                            has_conflict = True
                            summary_report.append(f"Category '{slug}': CONFLICT (data differs)")
                    except ContentCategory.DoesNotExist:
                        if not dry_run:
                            new_cat = ContentCategory.objects.create(**cat_data)
                            category_map[slug] = new_cat
                        summary_report.append(f"Category '{slug}': CREATE")

                # 2. Process Articles
                for art_data in CANONICAL_ARTICLES:
                    slug = art_data["slug"]
                    cat_slug = art_data["category_slug"]
                    target_category = category_map.get(cat_slug) or ContentCategory.objects.filter(slug=cat_slug).first()

                    if not target_category and not dry_run:
                        has_conflict = True
                        summary_report.append(f"Article '{slug}': CONFLICT (category '{cat_slug}' missing)")
                        continue

                    try:
                        existing = Article.objects.get(slug=slug)
                        # Compare fields
                        if (
                            existing.title == art_data["title"]
                            and existing.article_type == art_data["article_type"]
                            and existing.category.slug == cat_slug
                            and existing.author.username == author.username
                            and existing.summary == art_data["summary"]
                            and existing.body == art_data["body"]
                            and existing.status == art_data["status"]
                        ):
                            summary_report.append(f"Article '{slug}': EXISTS")
                        else:
                            has_conflict = True
                            summary_report.append(f"Article '{slug}': CONFLICT (data differs)")
                    except Article.DoesNotExist:
                        if not dry_run:
                            pub_at = datetime.fromisoformat(art_data["published_at_iso"])
                            Article.objects.create(
                                title=art_data["title"],
                                slug=slug,
                                article_type=art_data["article_type"],
                                category=target_category,
                                author=author,
                                summary=art_data["summary"],
                                body=art_data["body"],
                                status=art_data["status"],
                                published_at=pub_at,
                            )
                        summary_report.append(f"Article '{slug}': CREATE")

                if has_conflict:
                    self.stderr.write(self.style.ERROR("\n".join(summary_report)))
                    raise CommandError("Conflict detected during content validation. Transaction aborted.")

                if dry_run:
                    transaction.set_rollback(True)

        except CommandError:
            raise
        except Exception as e:
            raise CommandError(f"Unexpected error during execution: {e}")

        self.stdout.write(self.style.SUCCESS("\n".join(summary_report)))
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN SUCCESSFUL: 0 database changes persisted."))
        else:
            self.stdout.write(self.style.SUCCESS("P1.3A editorial content loaded successfully."))
