from reprlib import recursive_repr

import requests
import random
import string
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.core import files
from io import BytesIO

from companies.models import Company, Markets, CompanyAddress
from custom.custom_tools2 import is_int, slugify


class Command(BaseCommand):

    def handle(self, *args, **options):
        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}

        url = 'https://www.crunchbase.com/organization/dropoff-inc'
        letters = string.ascii_lowercase
        random_str = ''.join(random.choice(letters) for i in range(8))
        content = session.get(url, verify=False).content
        soup = BeautifulSoup(content, "html.parser")
        general_info = soup.find('image-with-fields-card')
        company_name_cont = general_info.find('blob-formatter')
        company_name = company_name_cont.find('span').text
        company_info_cont1 = soup.find('fields-card')
        company_info_cont = company_info_cont1.find('div')
        company_infos = company_info_cont.findChildren('span', recursive=False)
        i = 1
        company_info_dict = {}
        for company_info in company_infos:
            if i % 2 == 1:
                company_info_label = company_info.text
            else:
                company_info_value = company_info.text
                company_info_dict[company_info_label] = company_info_value
            i = i + 1
        company_info_soc_cont1 = soup.findAll('fields-card')[2:3]
        company_info_soc_cont = company_info_soc_cont1[0].find('div')
        company_info_social1 = company_info_soc_cont.findChildren('span', recursive=False)
        j = 1
        for company_info_social in company_info_social1:
            if j % 2 == 1:
                company_info_soc_label = company_info_social.text
            else:
                if company_info_soc_label == 'Facebook\xa0' or company_info_soc_label == 'LinkedIn\xa0' or company_info_soc_label == 'Twitter\xa0':
                    company_info_soc_value = company_info_social.find('a', href=True)
                    company_info_soc_value = company_info_soc_value['href']
                else:
                    company_info_soc_value = company_info_social.text

                company_info_dict[company_info_soc_label] = company_info_soc_value
            j = j + 1
        desc_card = soup.find('description-card')
        print(desc_card)
        company_desc = desc_card.findAll('p')[0].text
        try:
            company_desc = company_desc + desc_card.findAll('p')[1].text
        except:
            company_desc = company_desc

        if company_info_dict['Website\xa0'] is not None:
            img_src = 'http://logo.clearbit.com/' + company_info_dict['Website\xa0']
            resp = requests.get(img_src)
            fp = BytesIO()
            fp.write(resp.content)
            file_name = slugify(company_name + random_str)
            # print(slugify(company_name+random_str))
        new_company = Company()

        if company_info_dict['Website\xa0'] is not None:
            new_company.company_logo.save(file_name, files.File(fp))
        if company_name is not None:
            new_company.name = company_name
        if company_desc is not None:
            new_company.info = company_desc
        if 'Website\xa0' in company_info_dict:
            new_company.website = company_info_dict['Website\xa0']
        if 'Founded Date\xa0' in company_info_dict:
            if is_int(company_info_dict['Founded Date\xa0']):
                new_company.founded = company_info_dict['Founded Date\xa0']
        if 'Number of Employees\xa0' in company_info_dict:
            employee_count = company_info_dict['Number of Employees\xa0'].split('-')[-1]
            if is_int(int(employee_count)):
                new_company.size = int(employee_count)
        if 'Facebook\xa0' in company_info_dict:
            new_company.facebook_url = company_info_dict['Facebook\xa0']
        if 'LinkedIn\xa0' in company_info_dict:
            new_company.linkedin_url = company_info_dict['LinkedIn\xa0']
        if 'Twitter\xa0' in company_info_dict:
            new_company.twitter_url = company_info_dict['Twitter\xa0']
        if 'Contact Email\xa0' in company_info_dict:
            new_company.contact_email = company_info_dict['Contact Email\xa0']
        if 'Phone Number\xa0' in company_info_dict:
            new_company.contact_number = company_info_dict['Phone Number\xa0']
        # new_company.slug = slugify(company_name+random_str)

        new_company.save()
        new_loc = CompanyAddress()
        if 'Headquarters Regions\xa0' in company_info_dict:
            # location = company_info_dict['Headquarters Regions\xa0'].split(',')
            new_loc = CompanyAddress()
            new_loc.location = company_info_dict['Headquarters Regions\xa0']
            new_loc.save()

        new_company.location.add(new_loc)
        catexp = company_info_dict['Industries\xa0'].split(',')

        for market_name in catexp:
            new_market = Markets()
            if Markets.objects.filter(market_name=market_name).exists():
                new_company.markets.add(Markets.objects.get(market_name=market_name))
            else:
                new_market.market_name = market_name
                new_market.save()
                new_company.markets.add(new_market)
