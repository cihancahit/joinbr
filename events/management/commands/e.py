import uuid
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from imagekit import files

from events.models import Category, Event
from joinbro import settings

CATEGORIES = {
    '103': 'MUSIC',
    '101': 'CAREER & BUSINESS',
    '110': 'FOOD & BEVERAGES',
    '113': 'SOCIAL',
    '105': 'POETRY',
    '104': 'MOVIES',
    '108': 'SPORTS & FITNESS',
    '107': 'HEALTH & WELLNESS',
    '102': 'TECH',
    '109': 'OUTDOORS & ADVENTURE',
    '111': 'OTHER',
    '114': 'OTHER',
    '115': 'FAMILY',
    '116': 'OTHER',
    '112': 'OTHER',
    '106': 'FASHION & BEAUTY',
    '117': 'OTHER',
    '118': 'OTHER',
    '119': 'OTHER',
    '199': 'OTHER',
    '120': 'LEARNING',
}


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('event_url', type=str)
        parser.add_argument('page_count', type=int)

    def handle(self, *args, **options):
        auth_token = settings.EB_AUTH_TOKEN
        pc = options['page_count']
        session = requests.Session()
        for event in Event.objects.all():
            event.delete()

        session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
        for i in range(1, pc):
            url = options['event_url'] + '?page=' + str(i)

            content = session.get(url, verify=False).content

            soup = BeautifulSoup(content, "html.parser")

            table = soup.find('ul', {'class': 'search-main-content__events-list'})  # returns a list
            # thead = table.findChild('thead', recursive=False)
            trs = table.findChildren('li', recursive=False)
            for li in trs:
                a = li.findChildren('a')[0]
                link = a.get('href')
                start = link.rfind('-') + 1
                end = link.rfind('?')
                event_id = link[start:end]
                # print(event_id)
                url = 'https://www.eventbriteapi.com/v3/events/' + event_id
                header = {'Authorization': 'Bearer ' + auth_token}
                r = requests.get(url=url, headers=header)
                if r.status_code == 200:
                    event = r.json()
                    name = event['name']
                    name_text = name['text']  # use this as name
                    print(name_text)
                    name_text = name_text[:254]
                    desc = event['description']
                    desc_text = desc['html']  # event info
                    event_url = event['url']
                    start_time = event['start']
                    start_time_utc = start_time['utc']  # use this as start time
                    end_time = event['end']
                    end_time_utc = end_time['utc']  # use this as end time
                    is_free = event['is_free']
                    price = 0
                    if is_free == 'true':
                        ticket_type = 'free'
                        price = 0
                    else:
                        ticket_type = 'paid'
                    if event['logo']:
                        logo = event['logo']
                        original = logo['original']
                        logo_url = original['url']
                    else:
                        logo_url = 'https://www.revealin.com/static/assets/images/no-photo.png'
                    resp = requests.get(logo_url)
                    fp = BytesIO()
                    fp.write(resp.content)
                    file_name = str(uuid.uuid4())
                    cat_id = event['category_id']
                    event_cat_name = CATEGORIES.get(str(cat_id))
                    venue_id = event['venue_id']
                    # print("venue id: " + str(venue_id))
                    if not venue_id == 'null':
                        venue_endpoint_url = 'https://www.eventbriteapi.com/v3/venues/' + str(venue_id) + '/'
                        r1 = requests.get(url=venue_endpoint_url, headers=header)
                        if r1.status_code == 200:
                            b1 = r1.json()
                            venue_address = b1['address']
                            venue_address1 = venue_address['address_1']
                            venue_loc_city = venue_address['city']
                            venue_loc_country_code = venue_address['country']
                            venue_lat = venue_address['latitude']
                            venue_lon = venue_address['longitude']
                            venue_name = b1['name']
                    # saving content to event
                    new_event = Event()
                    new_event.name = name_text
                    new_event.info = desc_text
                    new_event.start_event_dt = start_time_utc
                    new_event.finish_event_dt = end_time_utc
                    new_event.ticket_type = ticket_type
                    if price:
                        new_event.price = price
                    new_event.event_img.save(file_name, files.File(fp))
                    if not venue_id == 'null':
                        new_event.city = venue_loc_city
                        new_event.country = venue_loc_country_code
                        new_event.location = venue_address1
                    if Category.objects.filter(name=event_cat_name).exists():
                        new_event.category.add(Category.objects.get(name=event_cat_name))
                    new_event.save()
