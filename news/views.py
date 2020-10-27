import feedparser
import requests
from django.shortcuts import redirect
from django.views.generic import TemplateView

from fec_app.views import BaseContext
from news.models import News
from users.models import UserProfileModel, UserRSS


class ArticleView(BaseContext, TemplateView):
    template_name = "pages/other/all_news.html"

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context["articles"] = News.objects.all()
        context["main_article"] = News.objects.filter(sponsored=True)
        context["news_active"] = "menu-active"
        diclist = []
        if self.request.user.is_authenticated:
            rss1 = UserProfileModel.objects.get(user=self.request.user)
            for rss_link in rss1.rss.all():
                feed = feedparser.parse(rss_link.rss_link)
                keys = ["title", "link", "description"]
                for i in range(0, 5):

                    if feed['entries'][i]:
                        values = [feed['entries'][i].title, feed['entries'][i].link, feed['entries'][i].description]
                        diclist.append(dict(zip(keys, values)))
        context["rss"] = diclist
        return context


def add_rss(request, ):
    if request.method == 'POST':
        redirect_url = "news"
        url = 'https://cloud.feedly.com/v3/search/feeds/'
        params = {'query': request.POST.get("rss-link")}
        r = requests.get(url=url, params=params)
        if r.status_code == 200:
            b = r.json()
            c = b['results']
            if len(c) > 0:
                a = c[0]['feedId']

                rss_link = UserRSS.objects.create(
                    title="user_rss",
                    rss_link=a[5:]
                )
                user_profile = UserProfileModel.objects.get(user=request.user)

                user_profile.rss.add(rss_link)

    return redirect(redirect_url)
