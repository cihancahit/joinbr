import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.core import files
from io import BytesIO

from companies.models import Company, Markets, CompanyAddress
from custom.custom_tools2 import is_int,slugify


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('maxpagenum', type=int)
        parser.add_argument('pagestart', type=int)
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}

        # url1 = options['url']
        pagenum = options['maxpagenum']
        ps = options['pagestart']
        for i in range(ps, pagenum):

            url = options['url'] + '?pageSize=100&orderBy=1&filterByPost=false&currentPage=' + str(i)

            content = session.get(url, verify=False).content
            soup = BeautifulSoup(content, "html.parser")
            comcon = soup.find('div', {'class': 'SPList'})
            uls = comcon.findChildren('ul', recursive=False)
            for ul in uls:
                name = ''
                about = ''
                website = ''
                catexp = []
                location = ''
                founded = ''
                link = ul.find('a', {'class': 'profileNavigator'})

                company_link = 'https://www.globaltrade.net/' + link['href']
                print(company_link)
                content_detail = session.get(company_link, verify=False).content
                soup_detail = BeautifulSoup(content_detail, "html.parser")
                if not soup_detail.find('div',{'class':'profile-image'}):
                    continue
                img_container = soup_detail.find('div',{'class':'profile-image'})
                img2 = img_container.find('div',{'class':'image'})
                img_src = '/static/assets/images/no_photo.png'
                if img2.find('img',{'class': 'lazy'}):
                    imgtag = img2.find('img', {'class': 'lazy'})
                    img_src = imgtag['data-original']
                    resp = requests.get(img_src)
                    fp = BytesIO()
                    fp.write(resp.content)

                file_name = img_src.split("/")[-1]
                container = soup_detail.find('div', {'class': 'col-01'})
                title1 = container.find('h1', {'class': 'sp-title'})
                name = title1.find('span').text
                print("22222222")
                print(name)
                print("3333333333")
                if Company.objects.filter(name=name).exists():
                    print(name)
                    continue

                profile_detail = soup_detail.find('div', {'class': 'profile-content'})
                table = profile_detail.find('table')

                trs = table.findChildren('tr', recursive=False)
                list_len = len(trs)

                for i in range(list_len):
                    tr = table.findChildren('tr', recursive=False)[i]
                    td = tr.findChildren('td', recursive=False)[0].text
                    if td.strip().lower() == 'about:':
                        about1 = tr.findChildren('td', recursive=False)[1].text
                        about = about1
                    if td.strip().lower() == 'website:':
                        websitetd = tr.findChildren('td', recursive=False)[1]
                        website = websitetd.find('a')['href']
                    if td.strip().lower() == 'category of expertise:':
                        catexp1 = tr.findChildren('td', recursive=False)[1]
                        eps = catexp1.findChildren('a')
                        for ep in eps:
                            catexp.append(ep.text)
                    if td.strip().lower() == 'primary location:':
                        location = tr.findChildren('td', recursive=False)[1].text
                    if td.strip().lower() == 'date of creation:':
                        founded = tr.findChildren('td', recursive=False)[1].text
                        founded = founded[-4:]

                new_company = Company()

                # new_expert.expert_img.save(new_file, files.File(fp))
                # new_company.expert_img.save(file_name, files.File(fp))
                if len(img_src) > 0 and img2.find('img',{'class':'lazy'}):
                    new_company.company_logo.save(file_name, files.File(fp))
                if len(name) > 0:
                    new_company.name = name
                if len(about) > 0:
                    new_company.info = about.strip()
                if len(website) > 0:
                    new_company.website = website.strip()
                if len(founded) > 0:
                    if is_int(founded):
                        new_company.founded = founded
                new_company.slug = slugify(name)

                new_company.save()
                new_loc = CompanyAddress()
                if location.find(',') > 0:
                    location = location.split(',')
                    new_loc = CompanyAddress()
                    new_loc.city = location[0]
                    new_loc.country = location[1]
                    new_loc.save()
                else:
                    new_loc.country = location
                    new_loc.save()
                new_company.location.add(new_loc)

                for market_name in catexp:
                    new_market = Markets()
                    if Markets.objects.filter(market_name=market_name).exists():
                        new_company.markets.add(Markets.objects.get(market_name=market_name))
                    else:
                        new_market.market_name = market_name
                        new_market.save()
                        new_company.markets.add(new_market)
