from django.urls import path, include
from .views import *
urlpatterns = [
    path('', IndexView.as_view(), name="index_url"),
    path('ac/search/c/country', ac_search_c_country, name="autofill_country"),
    path('ac/search/c/city', ac_search_c_city, name="autofill_city"),
    path('ac/search/language', ac_search_lang, name="autofill_language"),
    path('cc/', comingSoon, name="comingsoon"),
    path('emailsubmit/', emailSubmit, name="emailsubmit"),
    path('import-data/', ImportCompany.as_view(), name="import_company"),
    path('terms-conditions/', terms, name="terms"),
    path('privacy/', privacy, name="privacy"),
    path('faq/', faq, name="faq"),
    path('about/', about, name="about"),
]
