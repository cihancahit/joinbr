import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
        pagenum = 2
        url = 'http://www.world-businessdirectory.com/results.php?p='
        for i in range(1, pagenum):
            new_link = url + str(i)
            print(new_link)
            content = session.get(new_link, verify=False).content
            soup = BeautifulSoup(content, "html.parser")
            t1 = soup.find('div', {'id': 'content_inner'})
            t2 = t1.find('tr')
            t3 = t2.find_all('td')[0::1]
            print(t3)