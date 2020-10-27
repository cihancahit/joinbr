from _threading_local import local
from io import BytesIO
import time
import uuid

import requests
from django.core.management.base import BaseCommand
from imagekit import files

from events.models import Event, Category


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('cat', type=int)
        parser.add_argument('pagestart', type=int)
        parser.add_argument('pagecount', type=int)

    def handle(self, *args, **options):
        pagecount = options['pagecount']
        ps = options['pagestart']
        categories = {
            '105': 'Art',
            '106': 'Fashion',
            '103': 'Music',
            '101': 'Business',
            '108': 'Sport',
            '110': 'Food&Drink',
        }
        event_cat_name = categories.get(str(options['cat']))
        event_cat_name = str(event_cat_name)
        for i in range(ps, pagecount):
            url = 'https://www.eventbriteapi.com/v3/events/search/'
            params = {'categories': options['cat'], 'page': str(i), 'token': '3HZOTG3CP7FR3HDACQYP'}
            r = requests.get(url=url, params=params)

            if r.status_code == 200:
                b = r.json()
                events = b['events']
                i = 0
                for event in events:
                    print(i)
                    i = i +1
                    name = event['name']
                    name_text = name['text']  # use this as name
                    name_text = name_text[:254]
                    desc = event['description']
                    desc_text = desc['html']  # event info
                    event_url = event['url']
                    start_time = event['start']
                    start_time_utc = start_time['utc'] #use this as start time
                    end_time = event['end']
                    end_time_utc = end_time['utc'] #use this as end time
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
                    venue_id = event['venue_id']
                    if not venue_id == 'null':
                        venue_endpoint_url = 'https://www.eventbriteapi.com/v3/venues/' + str(venue_id) + '/'
                        params1 = {'token': '3HZOTG3CP7FR3HDACQYP'}
                        r1 = requests.get(url=venue_endpoint_url, params=params1)

                        if r1.status_code == 200:
                            b1 = r1.json()
                            venue_address = b1['address']
                            venue_address1 = venue_address['address_1']
                            venue_loc_city = venue_address['city']
                            venue_loc_country_code = venue_address['country']
                            venue_lat = venue_address['latitude']
                            venue_lon = venue_address['longitude']
                            venue_name = b1['name']


                    #saving content to event
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
                        new_event.location = venue_loc_country_code
                    if Category.objects.filter(name=event_cat_name).exists():
                        new_event.category.add(Category.objects.get(name=event_cat_name))

                    new_event.save()
