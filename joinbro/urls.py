from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.contrib.sitemaps import views
from django.views.generic import TemplateView

from joinbro import settings
from fec_app.views import handler404
from fec_app.sitemaps import *


sitemaps = {
    'static': StaticViewSitemap,
    'flatpages': FlatPagesSitemap,
    'event': EventSitemap,
    'expert': ExpertSitemap,
    'company': CompanySitemap,
}


handler404 = handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('fec_app.urls')),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('experts/', include('expert.urls')),
    path('', include('news.urls')),
    path('companies/', include('companies.urls')),
    path('review/', include('reviews_and_rating.urls')),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="pages/other/robots.txt", content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
