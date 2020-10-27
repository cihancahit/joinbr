
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        filename = os.path.join(os.path.dirname(__file__), 'city.txt')
        city_file = open(filename)

        # lists to hold zip code, longitude and latitude values:

        iso_codes = []
        city_names = []

        for line in city_file.readlines():
            print('fips:' + line[:2])
            print('iso:' + line[3:5])
            print('name:' + line[6:])

