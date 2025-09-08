from django.core.management import call_command
from django.core.management.base import BaseCommand
from mama_to_be.common.utils.signal_control import disable_seed_signals

class Command(BaseCommand):
    help = "Seed initial data into the database"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding DB..."))

        with disable_seed_signals():
            call_command("loaddata", "seed.json")
        
        self.stdout.write(self.style.SUCCESS("Seed complete."))
