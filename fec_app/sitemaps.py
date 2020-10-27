from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from companies.models import Company
from events.models import Event
from expert.models import Expert


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['terms', 'privacy', 'faq', 'about']

    def location(self, item):
        return reverse(item)


class FlatPagesSitemap(Sitemap):
    priority = 0.8
    changefreq = 'hourly'

    def items(self):
        return ['index_url', 'AllEvents', 'expert', 'new_expert', 'companies', 'add_company']

    def location(self, item):
        return reverse(item)


class EventSitemap(Sitemap):
    changefreq = 'hourly'

    def items(self):
        return Event.objects.all()

    def location(self, item):
        return reverse('event_detail_url', args=[item.slug])


class ExpertSitemap(Sitemap):
    changefreq = 'hourly'

    def items(self):
        return Expert.objects.all()

    def location(self, item):
        return reverse('expert_detail', args=[item.slug])


class CompanySitemap(Sitemap):
    changefreq = 'hourly'

    def items(self):
        return Company.objects.all()

    def location(self, item):
        return reverse('company_detail', args=[item.slug])
