from django.urls import path

from .views import *

urlpatterns = [
    path('profile/<slug:slug>/edit', CompanyProfileEditView.as_view(), name="company_profile_edit"),
    path('', CompanyView.as_view(), name="companies"),
    path('search', CompanySearchView.as_view(), name="company_search"),
    path('<slug:slug>', CompanyDetailView.as_view(), name="company_detail"),
    # path('country/<str:country>/<str:city>', company_search_city, name="company_search_city"),
    # path('<str:market>/<str:country>/<str:city>', company_search_3, name="company_search"),
    path('market/<str:market>', company_search_market, name="company_search_market"),
    path('location/<str:location>', company_search_country, name="company_search_country"),
    path('<str:market>/<str:location>', company_search_market_country, name="company_search_market_country"),
    path('ac/search/c/name', ac_search_c_name, name="ac_company_name"),
    path('ac/search/c/market', ac_search_c_market, name="ac_company_market"),
    path('company-list', company_list, name="company_list"),
    path('<slug:slug>/follow', CompanyFollowAPIToggle.as_view(), name="company_follow"),
    path('ac/search/c/name/profile', ac_search_c_name_profile, name="ac_company_name"),
    path('new/', NewCompanyView.as_view(), name="new_company"),
    path('add_company/', add_company, name="add_company"),
    path('import-excel/', ImportCompanyExcelList.as_view(), name="import_company_excel_list"),
]
