from django.core.management import call_command
from django.core.management.base import BaseCommand
from mama_to_be.common.utils.signal_control import disable_seed_signals

class Command(BaseCommand):
    help = "Load seed data without triggering signals"

    def handle(self, *args, **options):
        with disable_seed_signals():
            call_command("loaddata", "seed.json")