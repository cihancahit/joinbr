from django.urls import path, include
from .views import ArticleView, add_rss

urlpatterns = [
    path('news', ArticleView.as_view(), name="news"),
    path('news/add', add_rss, name="add_rss"),
]
