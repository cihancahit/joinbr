from reprlib import recursive_repr

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.core import files
from io import BytesIO

from expert.models import Expert
from custom.custom_tools2 import is_int, slugify


class Command(BaseCommand):

    def handle(self, *args, **options):
        proxies = {"http": "http://193.165.118.38:35655",
                   "https": "http://45.187.67.254:43024"}
        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}

        url = 'https://www.crunchbase.com/person/brandon-dawson'

        content = requests.get(url, verify=False,proxies=proxies).content
        soup = BeautifulSoup(content, "html.parser")
        print(soup)
        general_info = soup.find('image-with-fields-card')
        expert_name_cont = general_info.find('blob-formatter')
        expert_business_title1 = general_info.findAll('field-formatter')[1:2]
        if expert_business_title1 is not None:
            for btitle in expert_business_title1:
                expert_business_title = btitle.text
        expert_name = expert_name_cont.find('span').text
        expert_info_cont1 = soup.find('fields-card')
        expert_info_cont = expert_info_cont1.find('div')
        expert_infos = expert_info_cont.findChildren('span', recursive=False)
        i = 1
        expert_info_dict = {}
        for expert_info in expert_infos:
            if i % 2 == 1:
                expert_info_label = expert_info.text
            else:
                expert_info_value = expert_info.text
                expert_info_dict[expert_info_label] = expert_info_value
            i = i + 1
        expert_info_soc_cont1 = soup.findAll('fields-card')[1:2]
        expert_info_soc_cont = expert_info_soc_cont1[0].find('div')
        expert_info_social1 = expert_info_soc_cont.findChildren('span', recursive=False)
        j = 1
        for expert_info_social in expert_info_social1:
            if j % 2 == 1:
                expert_info_soc_label = expert_info_social.text
            else:
                if expert_info_soc_label == 'Facebook\xa0' or expert_info_soc_label == 'LinkedIn\xa0' or expert_info_soc_label == 'Twitter\xa0':
                    expert_info_soc_value = expert_info_social.find('a', href=True)
                    expert_info_soc_value = expert_info_soc_value['href']
                else:
                    expert_info_soc_value = expert_info_social.text

                expert_info_dict[expert_info_soc_label] = expert_info_soc_value
            j = j + 1
        desc_card = soup.find('description-card')
        expert_desc = desc_card.findAll('p')[0].text
        expert_desc = expert_desc + desc_card.findAll('p')[1].text
        new_expert = Expert()
        if expert_name is not None:
            new_expert.name = expert_name
        if expert_desc is not None:
            new_expert.bio = expert_desc
        if expert_business_title is not None:
            new_expert.business_title = expert_business_title
        if 'Website\xa0' in expert_info_dict:
            new_expert.personal_url = expert_info_dict['Website\xa0']
        if 'Facebook\xa0' in expert_info_dict:
            new_expert.facebook_url = expert_info_dict['Facebook\xa0']
        if 'Linkedin\xa0' in expert_info_dict:
            new_expert.linkedin_url = expert_info_dict['Linkedin\xa0']
        if 'Twitter\xa0' in expert_info_dict:
            new_expert.twitter_url = expert_info_dict['Twitter\xa0']
        if 'Location\xa0' in expert_info_dict:
            new_expert.location = expert_info_dict['Location\xa0']
        new_expert.save()