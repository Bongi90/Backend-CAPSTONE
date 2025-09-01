from django.core.management.base import BaseCommand
from kids_todo.models import TaskTemplate

DEFAULTS = [
    ("Wake up", "BEFORE"),
    ("Brush teeth", "BEFORE"),
    ("Eat breakfast", "BEFORE"),
    ("Get dressed", "BEFORE"),
    ("Pack school bag", "BEFORE"),
    ("Do homework", "AFTER"),
    ("Clean up room", "AFTER"),
    ("Have supper", "AFTER"),
    ("Shower", "AFTER"),
]

class Command(BaseCommand):
    help = "Seed default Before/After school task templates"

    def handle(self, *args, **options):
        created = 0
        for i, (title, category) in enumerate(DEFAULTS):
            obj, was_created = TaskTemplate.objects.get_or_create(
                title=title, defaults={"category": category, "order": i}
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} templates."))
