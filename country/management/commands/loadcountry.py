import os

from django.core.management.base import BaseCommand

from country.models import Country


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        filename = os.path.join(os.path.dirname(__file__), 'country.txt')
        country_file = open(filename)

        # lists to hold zip code, longitude and latitude values:

        cc_fipss = []
        cc_isos = []
        tlds = []
        names = []

        for line in country_file.readlines():
            cc_fips, cc_iso, tld, name = line.strip().split(',')

            cc_fipss.append(cc_fips)
            cc_isos.append(cc_iso)
            tlds.append(tld)
            names.append(name)

        counter = 0
        for i in Country.objects.all():
            i.delete()

        for item in cc_fipss:
            country_object = Country(cc_fips=cc_fipss[counter], cc_iso=cc_isos[counter], tld=tlds[counter],
                                     name=names[counter])
            country_object.save()
            counter = counter + 1
