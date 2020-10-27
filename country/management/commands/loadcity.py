import os

from django.core.management.base import BaseCommand

from country.models import Country, City


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        filename = os.path.join(os.path.dirname(__file__), 'city.txt')
        city_file = open(filename, encoding="utf8")

        # lists to hold zip code, longitude and latitude values:

        for i in City.objects.all():
            i.delete()

        for line in city_file.readlines():
            cc_fips = line[:2]
            cc_iso = line[3:5]
            name = line[6:]

            country = Country.objects.get(cc_iso=cc_iso)
            city_object = City(country=country, name=name)
            city_object.save()
