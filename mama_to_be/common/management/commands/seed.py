from django.core.management import call_command
from django.core.management.base import BaseCommand
from mama_to_be.common.utils.signal_control import disable_seed_signals
from mama_to_be.common.utils import signal_control

class Command(BaseCommand):
    help = "Seed initial data into the database"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding DB..."))

        signal_control.DISABLE_SEED_SIGNALS = True
        try:
            call_command("loaddata", "seed.json")
        finally:
            signal_control.DISABLE_SEED_SIGNALS = False
        
        self.stdout.write(self.style.SUCCESS("Seed complete."))
