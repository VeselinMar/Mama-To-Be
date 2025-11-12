from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.management import call_command
import io


def dump_seed():
    out = io.StringIO()
    call_command(
        "dumpdata",
        "profiles.AppUser",
        "articles.Article",
        indent=2,
        stdout=out,
    )

    with open("seed.json", "w", encoding="utf-8") as f:
        f.write(out.getvalue())