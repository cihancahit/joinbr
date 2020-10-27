import os
from time import time

from PIL import Image

import urllib3
import re, socket
from django.contrib.gis.geoip2 import GeoIP2


def getUserCity(ip):
    g = GeoIP2()
    location = g.city(ip)
    location_city = location["city"]
    print(location_city)
    if location_city is not None:
        city = 'Events in <span>'+location_city+'</span> <span style="text-transform: lowercase; color: #3f3f3f;font-family: \'Lato Black\'">or closeby</span>'
    else:
        city = 'Events you may like'
    return city


def get_news_img_path(instance, filename):
    return "news/%s_%s" % (str(time()).replace('.', '_'), filename.replace(' ', '_'))


def get_company_logo_path(instance, filename):
    return "company/%s_%s" % (str(time()).replace('.', '_'), filename.replace(' ', '_'))


def get_companyproduct_img_path(instance, filename):
    return "company/product/%s_%s" % (str(time()).replace('.', '_'), filename.replace(' ', '_'))


def get_expert_img_path(instance, filename):
    return "expert/%s_%s" % (str(time()).replace('.', '_'), filename.replace(' ', '_'))


def get_event_img_path(instance, filename):
    return "event/%s_%s" % (str(time()).replace('.', '_'), filename.replace(' ', '_'))


def get_category_img_path(instance, filename):
    return "category/%s_%s" % (str(time()).replace('.', '_'), filename.replace(' ', '_'))


def get_profile_img_path(instance, filename):
    return "profile/%s_%s" % (str(time()).replace('.', '_'), filename.replace(' ', '_'))


def add_logo(mfname, lfname, outfname):
    mimage = Image.open(mfname)
    limage = Image.open(lfname)

    # resize logo
    wsize = int(min(mimage.size[0], mimage.size[1]) * 0.25)
    wpercent = (wsize / float(limage.size[0]))
    hsize = int((float(limage.size[1]) * float(wpercent)))

    simage = limage.resize((wsize, hsize))
    mbox = mimage.getbbox()
    sbox = simage.getbbox()

    # right bottom corner
    box = (mbox[2] - sbox[2], mbox[3] - sbox[3])
    mimage.paste(simage, box)
    mimage.save(outfname)
    return outfname


def get_logo():
    return os.path.normpath("/static/assets/images/logo_small.png")


def slugify(title):
    symbol_mapping = (
        (' ', '-'),
        ('.', '-'),
        (',', '-'),
        (')', '-'),
        ('(', '-'),
        ('!', '-'),
        ('?', '-'),
        ('&', '-'),
        ("'", '-'),
        ('"', '-'),
        ('ə', 'e'),
        ('ı', 'i'),
        ('ö', 'o'),
        ('ğ', 'g'),
        ('ü', 'u'),
        ('ş', 's'),
        ('ç', 'c'),
    )
    title_url = title.strip().lower()

    for before, after in symbol_mapping:
        title_url = title_url.replace(before, after)

    return title_url
