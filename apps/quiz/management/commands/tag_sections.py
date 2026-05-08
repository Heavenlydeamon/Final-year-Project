"""
Django management command: tag_sections
----------------------------------------
Tags all MCQQuestions to their matching section_id and
populates Topic.sections JSONField based on the layout used in topic_study.html.

Usage:
    python manage.py tag_sections
    python manage.py tag_sections --dry-run    (preview without saving)
"""

from django.core.management.base import BaseCommand
from quiz.models import Quiz, MCQQuestion


# ─── Section Definitions ──────────────────────────────────────────────────────

GHATS_SECTIONS = [
    {"id": "intro",     "label": "Overview"},
    {"id": "formation", "label": "Formation History"},
    {"id": "wildlife",  "label": "Wildlife Spotlight"},
    {"id": "heritage",  "label": "Heritage Anchor"},
    {"id": "registry",  "label": "Registry: Landscapes"},
    {"id": "tribal",    "label": "Tribal Wisdom"},
    {"id": "threats",   "label": "Anthropogenic Pressure"},
    {"id": "climate",   "label": "Climate Resilience"},
]

LOWLANDS_SECTIONS = [
    {"id": "intro",       "label": "Overview"},
    {"id": "formation",   "label": "Formation History"},
    {"id": "casestudies", "label": "Case Studies"},
    {"id": "heritage",    "label": "Heritage Anchor"},
    {"id": "registry",    "label": "Registry: Examples"},
]

MIDLANDS_SECTIONS = [
    {"id": "intro",     "label": "Overview"},
    {"id": "formation", "label": "Formation History"},
    {"id": "wildlife",  "label": "Wildlife Spotlight"},
    {"id": "heritage",  "label": "Heritage Anchor"},
    {"id": "registry",  "label": "Registry: Examples"},
]

HERITAGE_SECTIONS = [
    {"id": "intro",      "label": "Overview"},
    {"id": "genesis",    "label": "Historical Genesis"},
    {"id": "mastery",    "label": "The Master's Touch"},
    {"id": "sacred",     "label": "Sacred Chronicles"},
    {"id": "collection", "label": "Collection Focus"},
    {"id": "registry",   "label": "Heritage Registry"},
]

CULTURAL_SECTIONS = [
    {"id": "intro",      "label": "Overview"},
    {"id": "genesis",    "label": "Historical Genesis"},
    {"id": "mastery",    "label": "The Master's Touch"},
    {"id": "sacred",     "label": "Sacred Chronicles"},
    {"id": "collection", "label": "Collection Focus"},
    {"id": "registry",   "label": "Culture Registry"},
]


# ─── Keyword → Section Maps ───────────────────────────────────────────────────

GHATS_KEYWORD_SECTION = [
    (["Sahyadri", "Himalayas", "mountain", "monsoon", "rain", "hydroelectric",
      "escarpment", "Carbon sink", "UNESCO", "Biodiversity Hotspot",
      "World Heritage", "perennial river", "Orographic", "1,600 km",
      "other name"], "intro"),
    (["Shola", "Grassland Mosaic", "Gondwana", "Podocarp", "Pleistocene",
      "formation", "lateritic", "soil", "geological", "1500m", "Sponge Effect",
      "Shola-Grassland", "high altitudes", "Neolithic", "petroglyph",
      "6,000 BCE"], "formation"),
    (["Nilgiri Tahr", "Lion-tailed Macaque", "Purple Frog", "Hornbill",
      "Flying Lizard", "endemic", "wildlife", "species", "frog",
      "living fossil", "canopy", "Forest Engineer", "Patal", "2003",
      "seeds", "highest peak", "rare frog", "underground"], "wildlife"),
    (["tribe", "tribal", "Kudi", "Adivasi", "indigenous",
      "traditional knowledge", "TEK", "minimal-footprint",
      "minimal footprint"], "tribal"),
    (["threat", "deforestation", "encroachment", "anthropogenic",
      "pressure", "invasive"], "threats"),
    (["climate", "carbon", "temperature", "warming",
      "resilience", "CO2", "sequestration"], "climate"),
    (["heritage", "protected", "reserve", "national park",
      "prehistoric"], "heritage"),
]

CULTURAL_KEYWORD_SECTION = [
    (["origin", "century", "history", "developed", "founded", "ancient",
      "begin", "evolution", "tradition", "meaning", "term", "mean",
      "what type", "known for", "unique", "form", "genre", "what is",
      "define"], "genesis"),
    (["costume", "makeup", "attire", "dress", "color", "Vesham",
      "Pacha", "instrument", "rhythm", "percussion", "technique",
      "mudra", "eye", "movement", "expression", "master", "training",
      "Kalamandalam", "school", "academy", "special about",
      "percussion instrument"], "mastery"),
    (["story", "epic", "Mahabharata", "Ramayana", "mythology", "legend",
      "sacred", "festival", "ritual", "deity", "god", "temple",
      "worship", "offering", "spiritual", "sources of"], "sacred"),
    (["performance", "repertoire", "style", "show", "stage", "venue",
      "season", "calendar", "where was", "originally performed",
      "how many"], "collection"),
    (["Kerala", "UNESCO", "heritage", "art form", "classical",
      "folk", "region", "state"], "intro"),
]

HERITAGE_KEYWORD_SECTION = [
    (["established", "built", "year", "century", "founded", "Portuguese",
      "Dutch", "British", "ruler", "king", "dynasty", "colonial",
      "history", "origin", "captured", "1663"], "genesis"),
    (["architecture", "mural", "painting", "craftsman", "style", "design",
      "construction", "material", "wood", "stone", "master",
      "Dutch Palace", "Mattancherry"], "mastery"),
    (["church", "temple", "mosque", "sacred", "ritual", "worship",
      "Chinese fishing", "Jewish", "community", "trade", "ancient",
      "spice", "Biennale", "Jew Street", "buried", "da Gama",
      "Francis Church"], "sacred"),
    (["collection", "exhibit", "artifact", "museum", "gallery",
      "visitor", "located", "area", "Malayalam", "nets called",
      "fishing net"], "collection"),
    (["what is", "which is", "oldest", "European", "India",
      "Kochi", "Fort", "known for"], "intro"),
]


# ─── Helper ───────────────────────────────────────────────────────────────────

def best_section(question_text, keyword_map, default="intro"):
    text_lower = question_text.lower()
    for keywords, section_id in keyword_map:
        for kw in keywords:
            if kw.lower() in text_lower:
                return section_id
    return default


# ─── Command ─────────────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = 'Tag all MCQQuestions to their section and populate Topic.sections'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview changes without saving to database',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN – no changes will be saved\n'))

        updated_topics = 0
        updated_questions = 0

        for quiz in Quiz.objects.select_related('topic').prefetch_related('questions').all():
            topic = quiz.topic
            title = topic.title
            category = topic.category

            # ── Pick layout ─────────────────────────────────────────────────
            if "Western Ghats" in title or "Highlands" in title:
                sections = GHATS_SECTIONS
                kw_map = GHATS_KEYWORD_SECTION
                layout = "ghats"
            elif "Lowlands" in title:
                sections = LOWLANDS_SECTIONS
                kw_map = []
                layout = "lowlands"
            elif "Midlands" in title or "Sea Level" in title or "Kuttanad" in title:
                sections = MIDLANDS_SECTIONS
                kw_map = []
                layout = "midlands"
            elif category == "heritage":
                sections = HERITAGE_SECTIONS
                kw_map = HERITAGE_KEYWORD_SECTION
                layout = "heritage"
            elif category == "artforms":
                sections = CULTURAL_SECTIONS
                kw_map = CULTURAL_KEYWORD_SECTION
                layout = "cultural"
            else:
                # Generic: distribute evenly across section-1/2/3
                q_list = list(quiz.questions.all())
                n = len(q_list)
                per_section = max(1, n // 3)
                sections = [
                    {"id": "section-1", "label": "Part 1"},
                    {"id": "section-2", "label": "Part 2"},
                    {"id": "section-3", "label": "Part 3"},
                ]
                kw_map = []
                layout = "generic"

                if not dry_run:
                    topic.sections = sections
                    topic.save(update_fields=["sections"])
                    updated_topics += 1

                for i, q in enumerate(q_list):
                    if i < per_section:
                        tag = "section-1"
                    elif i < per_section * 2:
                        tag = "section-2"
                    else:
                        tag = "section-3"
                    if not dry_run:
                        q.section_tag = tag
                        q.save(update_fields=["section_tag"])
                    updated_questions += 1

                self.stdout.write(
                    f"  [generic   ] {title[:45]:<45}  {n} q → section-1/2/3"
                )
                continue

            # ── Save topic sections ─────────────────────────────────────────
            if not dry_run:
                topic.sections = sections
                topic.save(update_fields=["sections"])
            updated_topics += 1

            # ── Tag questions ───────────────────────────────────────────────
            section_ids = [s["id"] for s in sections]
            questions = list(quiz.questions.all())

            tag_detail = []
            if kw_map:
                for q in questions:
                    tag = best_section(q.question_text, kw_map, default=section_ids[0])
                    if not dry_run:
                        q.section_tag = tag
                        q.save(update_fields=["section_tag"])
                    updated_questions += 1
                    tag_detail.append(f"{tag}")
                tag_method = "keyword"
            else:
                n = len(questions)
                per_sec = max(1, n // len(section_ids))
                for i, q in enumerate(questions):
                    idx = min(i // per_sec, len(section_ids) - 1)
                    tag = section_ids[idx]
                    if not dry_run:
                        q.section_tag = tag
                        q.save(update_fields=["section_tag"])
                    updated_questions += 1
                    tag_detail.append(tag)
                tag_method = "distributed"

            self.stdout.write(
                f"  [{layout:<10}] {title[:45]:<45}  "
                f"{len(questions)} q ({tag_method})"
            )
            if dry_run:
                for q, tag in zip(questions, tag_detail):
                    self.stdout.write(
                        f"               -> [{tag:<12}] {q.question_text[:65]}"
                    )

        self.stdout.write("")
        if dry_run:
            self.stdout.write(self.style.WARNING(
                f"DRY RUN complete. Would update {updated_topics} topics, "
                f"{updated_questions} questions."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Done!  Topics updated: {updated_topics}  |  "
                f"Questions tagged: {updated_questions}"
            ))
