from _threading_local import local

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from events.models import AggrEvents


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
        url = 'https://cryptocalendar.pro/'

        content = session.get(url, verify=False).content

        soup = BeautifulSoup(content, "html.parser")

        # table = soup.find('div', {'class': 'row'})  # returns a list
        # trs = table.findChildren('div', {'class': 'row '})
        #

        cimi = soup.find_all('div', {'class': 'col-lg-4 col-md-6 col-sm-6'})
        for tr in cimi:
            link = tr.find('a')
            link_url = link.get('href')
            user_link = 'https://cryptocalendar.pro' + link_url
            content_detail = session.get(user_link, verify=False).content
            soup_detail = BeautifulSoup(content_detail, "html.parser")
            title = soup_detail.find('h1', {'class': 'bold'}).text
            cdate = soup_detail.find('time').text
            content = soup_detail.find_all('p')[1].text
            new_event = AggrEvents()
            new_event.name = title
            # new_event.location = loc
            new_event.content = content
            new_event.startdate = cdate
            new_event.source = url
            new_event.save()