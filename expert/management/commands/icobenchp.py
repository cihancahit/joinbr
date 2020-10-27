from _threading_local import local
import random
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.core import files
from io import BytesIO
from custom.custom_tools import add_logo, get_logo

from expert.models import Expert

from django.db import IntegrityError


class Command(BaseCommand):
    # for blog in Expert.objects.all():
    #     blog.delete()

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('pagestart', type=int)

    def handle(self, *args, **options):
        ps = options["pagestart"]
        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}

        for i in range(ps, 4000):
            url = 'https://icobench.com/people?page=' + str(i)

            content = session.get(url, verify=False).content

            soup = BeautifulSoup(content, "html.parser")

            table = soup.find('table')  # returns a list
            if table:
                trs = table.findChildren('tr', recursive=False)

                for tr in trs:
                    ths = tr.findAll('td')
                    if ths is not None and len(ths) > 0:
                        title = ths[0]
                        link = title.find('a', {'class': 'image'})
                        user_link = 'https://icobench.com' + link['href']
                        content_detail = session.get(user_link, verify=False).content
                        soup_detail = BeautifulSoup(content_detail, "html.parser")
                        name = soup_detail.find('h1').text
                        business_title = soup_detail.find('h2').text
                        if soup_detail.find('div', {'class': 'location'}):
                            location = soup_detail.find('div', {'class': 'location'}).text
                        else:
                            location = ''
                        country = location.rsplit(',', 1)[len(location.rsplit(',', 1))-1]
                        twitter_url = soup_detail.find('a', {'class': 'twitter'})
                        if twitter_url:
                            twitter_url = twitter_url['href']
                        linkedin_url = soup_detail.find('a', {'class': 'linkedin'})
                        if linkedin_url:
                            linkedin_url = linkedin_url['href']
                        about_section = soup_detail.find('div', {'class': 'left'})
                        if about_section.find('p'):
                            bio = str(about_section.find('p'))
                        profile_img_div = soup_detail.find('div', {'class': 'image'})
                        profile_img = profile_img_div.find('img')
                        profile_img_url = profile_img['src']
                        # profile pic
                        resp = requests.get(profile_img_url)

                        fp = BytesIO()
                        fp.write(resp.content)
                        file_name = url.split("/")[-1]
                        # new_file = add_logo(files.File(fp), get_logo(), file_name)

                        new_expert = Expert()
                        # new_expert.expert_img.save(new_file, files.File(fp))
                        new_expert.expert_img.save(file_name, files.File(fp))
                        new_expert.business_title = business_title
                        new_expert.location = location
                        new_expert.country = country
                        new_expert.bio = bio
                        new_expert.twitter_url = twitter_url
                        new_expert.linkedin_url = linkedin_url
                        new_expert.is_approved = True
                        new_expert.name = name
                        new_expert.save_2()
