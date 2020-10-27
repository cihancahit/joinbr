import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}
        pagenum = 2
        url = options['url']

        # content = session.get(url, verify=False).content
        # soup = BeautifulSoup(content, "html.parser")
        print(url)
        #
