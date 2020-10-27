import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from events.models import AggrEvents


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
        url = 'https://www.cointelligence.com/content/events/'

        content = session.get(url, verify=False).content

        soup = BeautifulSoup(content, "html.parser")

        table = soup.find('section', {"class": "events-list-table"})  # returns a list
        # thead = table.findChild('tbody', recursive=False)
        trs = table.findChildren('ul',{"class":"single-event"})
        for tr in trs:
            title = tr.find('span').text
            cdate = tr.findChildren('li')[2].text
            loc = tr.findChildren('li')[4].text
            new_event = AggrEvents()
            new_event.name = title
            new_event.location = loc
            new_event.startdate = cdate
            new_event.source = url
            new_event.save()
