from django.urls import path
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('', ExpertView.as_view(), name="expert"),

    path('profile/<slug:slug>/myevents', ExpertProfileMyEventView.as_view(), name="expert_profile_myevent"),
    path('profile/<slug:slug>/edit/submit', ExpertUpdateProfile.as_view(), name="expert_profile_edit_submit"),
    path('profile/<slug:slug>', ExpertProfileView.as_view(), name="expert_profile"),
    path('profile/<slug:slug>/edit', ExpertProfileEditView.as_view(), name="expert_profile_edit"),
    path('profile/<slug:slug>/review', ExpertProfileEditView.as_view(), name="expert_profile_review"),
    path('ac/search/e/name/col', ac_search_e_name_col, name="ac_expert_name_col"),
    path('ac/search/e/name', ac_search_e_name, name="ac_expert_name"),
    path('ac/search/e/industry', ac_search_e_industry, name="ac_expert_industry"),
    path('ac/search/e/company', ac_search_e_company, name="ac_expert_company"),
    path('ac/search/e/skills', ac_search_e_skills, name="ac_expert_skills"),
    path('ac/search/e/lang', ac_search_e_lang, name="ac_expert_language"),
    path('api/experts/past_events/<slug:slug>', EventViewSet.as_view(), name="get_past_events"),
    path('search', ExpertSearchView.as_view(), name="expert_search"),
    path('<slug:slug>', ExpertDetailView.as_view(), name="expert_detail"),
    path('people/industry/<slug:slug>', ExpertViewMarket.as_view(), name="expert_industry"),
    path('people/company/<slug:slug>', ExpertViewCompany.as_view(), name="expert_company"),
    path('people/country/<slug:slug>', ExpertViewCountry.as_view(), name="expert_country"),
    path('add_expert/', add_expert, name="add_expert"),
    path('country/<str:country>', expert_search_country, name="expert_search_country"),
    path('language/<str:language>', expert_search_comp, name="expert_search_comp"),
    path('language/<str:language>/<str:country>/<str:city>', expert_search_c_c_i, name="expert_search_c_c_i"),
    path('country/<str:country>/<str:city>', expert_search_city, name="expert_search_city"),
    path('<str:skills>/language/<str:language>/<str:country>', expert_search_i_c_c, name="expert_search_i_c_c"),
    path('<str:skills>/<str:language>/<str:country>/<str:city>', expert_search_4, name="expert_search4"),
    path('skills/<str:skills>/<str:country>', expert_search_ind_country, name="expert_search_ind_country"),
    path('language/<str:language>/<str:country>', expert_search_comp_country, name="expert_search_ind_country"),
    path('<str:skills>/<str:country>/<str:city>', expert_search_3, name="expert_search3"),
    path('<str:skills>', expert_search_ind, name="expert_search_ind"),
    path('<str:skills>/<str:language>', expert_search_ind_comp, name="expert_search_ind_comp"),
    path('new/', NewExpertView.as_view(), name="new_expert"),
    path('linkedin-callback/', linkedin_auth, name="linkedin_auth"),
    path('api/experts/<slug:slug>/follow', ExpertFollowAPIToggle.as_view(), name="expert_follow"),
    path('api/experts/account_status/<slug:slug>', ExpertAccountStatus.as_view(), name="expert_account_status"),
    path('import-excel/', ImportExpertExcelList.as_view(), name="import_expert_excel_list"),
]
