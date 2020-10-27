import feedparser

from time import mktime
from datetime import datetime

from django.core.management.base import BaseCommand
from news.models import News
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Gets N recent blog posts. Better than parsing the list every page load.'

    def handle(self, *args, **options):
        num_blog_posts = 10
        for blog in News.objects.all():
            blog.delete()

        feed = feedparser.parse('https://atozmarkets.com/feed')

        loop_max = num_blog_posts if len(feed['entries']) > num_blog_posts else len(feed['entries'])

        for i in range(0, loop_max):
            if feed['entries'][i]:
                blog_post = News()
                blog_post.title = feed['entries'][i].title
                blog_post.link = feed['entries'][i].link
                blog_post.content = feed['entries'][i].description
                blog_post.publish_date = datetime.fromtimestamp(mktime(feed['entries'][i].published_parsed))
                blog_post.save()

        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
        url = 'https://atozmarkets.com/news'

        content = session.get(url, verify=False).content

        soup = BeautifulSoup(content, "html.parser")

        splash = soup.find('div', {'class': 'splash'})
        img_cont = splash.find('div', {'class': 'img-container'})
        img = img_cont.find('img', {'class': 'lozad'})
        img_link = img['data-src']
        div_text = splash.find('div', {'class': 'text'})
        h2_text = div_text.find('h2')
        link_g = h2_text.find('a')
        title = link_g.text
        link = link_g['href']
        publish_date = div_text.find('div', {'class': 'meta'}).text

        blog_post = News()
        blog_post.title = title
        blog_post.link = link
        blog_post.img_link = img_link
        blog_post.sponsored = True
        # blog_post.publish_date = datetime.fromtimestamp(mktime(publish_date.split("|", 1)[1]))
        blog_post.save()
