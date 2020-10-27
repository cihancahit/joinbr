from django.core.management.base import BaseCommand

from fec_app.languages import LANGUAGES

from fec_app.models import Languages


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in LANGUAGES:
            Languages.objects.create(
                language=LANGUAGES[i],
                iso_code=i,
            )
            print(i + "added to DB")
