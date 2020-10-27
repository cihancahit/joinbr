from datetime import datetime, timedelta
import json
import json as json2

import requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth, TruncDay, ExtractDay, Coalesce
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from hitcount.models import Hit
from hitcount.views import HitCountDetailView
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from events.forms import EventForm
from events.models import Tags, EventSponsors, Ticket
from fec_app.views import BaseContext
from organizer.models import Organizer
from users.AccessControl import ExpertRequiredMixin
from .models import *
from .serializers import ExpertEventSerializer
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse, HttpResponseForbidden
from io import BytesIO
from django.core import files
import traceback


class ExpertDetailView(BaseContext, HitCountDetailView):
    model = Expert
    template_name = 'pages/experts/expert_detail2.html'
    context_object_name = 'expert'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(ExpertDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        exp = Expert.objects.get(slug=slug)
        context["reviews"] = ReviewModel.objects.filter(expert__slug=slug)
        context["loggeduser"] = self.request.user
        context["date"] = datetime.today()
        # Similar Experts
        expert_skills = Expert.objects.get(slug=slug).fields_of_experties.all()
        if expert_skills.count() > 0:
            expert_skills2 = Expert.objects.filter(fields_of_experties=expert_skills[0]).exclude(slug=slug)[:2]
            context['similar_experts'] = expert_skills2
        # TODO country similairty will be added

        context['reviewer_tags'] = ExpertTags.objects.all()
        context["linkedin_auth_url"] \
            = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=" \
              + settings.CLIENT_ID \
              + "&redirect_uri=" + settings.REDIRECT_URI \
              + "&state=" + slug + "&scope=r_liteprofile%20r_emailaddress%20w_member_social"

        if Expert.objects.get(slug=slug).company:
            coll = Expert.objects.filter(company__expert=exp).exclude(slug=slug)[:2]
            context["partner_experts"] = coll

        if ExpertEvents.objects.filter(expert__slug=self.kwargs['slug']):
            context["events_f"] = ExpertEvents.objects.filter(expert__slug=self.kwargs['slug']).filter(
                event__start_event_dt__gt=datetime.today())[:3]
            # context["events_p"] = Event.objects.filter(speaker__slug=self.kwargs['slug']).filter(
            #     start_event_dt__lt=datetime.datetime.today())

        user = self.request.user
        context["expert_active"] = "menu-active"
        if user.is_authenticated:
            user1 = UserProfileModel.objects.get(user=user)
            context["logged_user"] = user1
            if user1 in exp.follower_list.all():
                context["expert_follow"] = "Unfollow"
            else:
                context["expert_follow"] = "Follow"
        else:
            context["logged_user"] = "anonymous"
            context["expert_follow"] = "Follow"

        return context


class ExpertView(BaseContext, ListView):
    template_name = "pages/experts/all_experts2.html"
    context_object_name = "experts"
    paginate_by = 10
    sort_type = 'alphabetic-asc'
    filter_type = '*'
    expert_list1 = {}

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        if self.request.GET.get('paginate_by'):
            self.request.session['pagee'] = self.request.GET.get('paginate_by')
        else:
            self.request.session['pagee'] = self.paginate_by
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        if self.request.GET.get('sort'):
            self.sort_type = self.request.GET.get('sort')
        if self.request.GET.get('filter'):
            self.filter_type = self.request.GET.get('filter')

        if self.filter_type == "*":
            expert_list = Expert.objects.all()
        elif self.filter_type == "full_time":
            expert_list = Expert.objects.filter(availability__type=300)
        elif self.filter_type == "freelance":
            expert_list = Expert.objects.filter(availability__type=200)
        elif self.filter_type == "agencies":
            expert_list = Expert.objects.filter(type__type=100)
        elif self.filter_type == "employee":
            expert_list = Expert.objects.filter(type__type=200)
        else:
            expert_list = Expert.objects.all()

        if self.sort_type == 'relevancy':
            # TODO relevancy will be added
            expert_list = expert_list.order_by("-id")
        elif self.sort_type == 'alphabetic-asc':
            expert_list = expert_list.order_by("name")
        elif self.sort_type == 'alphabetic-desc':
            expert_list = expert_list.order_by("-name")
        elif self.sort_type == 'popularity':
            # TODO popularity will be added
            expert_list = expert_list.order_by("id")
        else:
            expert_list = expert_list.order_by("-id")

        self.expert_list1 = expert_list
        return expert_list

    def get_context_data(self, **kwargs):
        context = super(ExpertView, self).get_context_data(**kwargs)

        context["companies"] = Company.objects.order_by("-avg_rating")[:4]
        context["expert_active"] = "menu-active"
        context["expert_count"] = self.expert_list1.count()
        if self.request.session.get('pagee'):
            context["pagee"] = self.request.session.get('pagee')

        context["sort_type"] = self.request.session['sort_type'] = self.sort_type
        return context


class ExpertViewMarket(BaseContext, ListView):
    template_name = "pages/experts/all_experts_market.html"
    context_object_name = "expertmarkets"
    paginate_by = 15

    def get_queryset(self):
        return Expert.objects.get_queryset().filter(industry__slug=self.kwargs['slug']).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super(ExpertViewMarket, self).get_context_data(**kwargs)

        context["slug"] = self.kwargs['slug']
        context["expert_active"] = "menu-active"
        return context


class ExpertViewCompany(BaseContext, ListView):
    template_name = "pages/experts/all_experts_company.html"
    context_object_name = "expertcompany"
    paginate_by = 15

    def get_queryset(self):
        return Expert.objects.get_queryset().filter(company__slug=self.kwargs['slug']).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super(ExpertViewCompany, self).get_context_data(**kwargs)

        context["slug"] = self.kwargs['slug']
        context["expert_active"] = "menu-active"
        return context


class ExpertViewCountry(BaseContext, ListView):
    template_name = "pages/experts/all_experts_country.html"
    context_object_name = "expertcountry"
    paginate_by = 15

    def get_queryset(self):
        return Expert.objects.filter(Q(country__icontains=self.kwargs['slug'])).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super(ExpertViewCountry, self).get_context_data(**kwargs)
        context["slug"] = self.kwargs['slug']
        context["expert_active"] = "menu-active"
        return context


class ExpertSearchView(BaseContext, ListView):
    template_name = "pages/experts/all_experts_search2.html"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(location__icontains=location)
        ).order_by("-id")
        return render(request, self.template_name, {
            'experts': experts, 'name': name,
            'expert_active': "active", 'location': location,
        })


def add_expert(request):
    if request.method == "POST":
        name = request.POST.get('name')
        btitle = request.POST.get('btitle')
        country = request.POST.get('country')
        city = request.POST.get('city')
        facebook = request.POST.get('facebook')
        linkedin = request.POST.get('linkedin')
        twitter = request.POST.get('twitter')
        website = request.POST.get('website')
        bio = request.POST.get('bio')
        contact = request.POST.get('contact')
        company = request.POST.get('company')
        expertise = request.POST.get('expertise')
        industry = request.POST.get('industry')
        age = request.POST.get('age')

        expertise = expertise.split(",")

        expert = Expert.objects.create(
            name=name,
            business_title=btitle,
            country=country,
            city=city,
            facebook_url=facebook,
            linkedin_url=linkedin,
            twitter_url=twitter,
            personal_url=website,
            bio=bio,
            age=age,
            contact=contact,
            expert_img=request.FILES.get('file'),
        )

        for i in expertise:
            tag = ExpertTags1.objects.create(
                expertise_fields=i
            )
            expert.fields_of_experties.add(tag)

        expert.company.add(Company.objects.get(name=company))
        expert.industry.add(Industries.objects.get(name=industry))
        expert.save()

        response_data = {'result': 'Create post successful!', }

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def expert_search_country(request, country, ):
    if request.POST:
        context = {}
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        country = country
        country = country.replace("-", " ")
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(country__icontains=country)
        ).order_by("-id")
        context["experts"] = experts
        context["name"] = name
        context["country"] = country
        context["location"] = location
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)
    else:
        return render(request, "pages/experts/all_experts_search2.html", )


def expert_search_city(request, country, city):
    if request.POST:
        context = {}
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        country = country
        city = city
        country = country.replace("-", " ")
        city = city.replace("-", " ")
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(country__icontains=country) &
            Q(city__icontains=city)
        ).order_by("-id")
        context["experts"] = experts
        context["name"] = name
        context["country"] = country
        context["city"] = city
        context["location"] = location
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)
    else:
        return render(request, "pages/experts/all_experts_search2.html", )


def expert_search_3(request, skills, country, city):
    if request.POST:
        context = {}
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        skills = skills
        country = country
        city = city
        country = country.replace("-", " ")
        skills = skills.replace("-", " ")
        city = city.replace("-", " ")
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(fields_of_experties__expertise_fields=skills) &  # fields_of_experties__expertise_fields
            Q(country__icontains=country) &
            Q(city__icontains=city)
        ).order_by("-id")
        context["experts"] = experts
        context["name"] = name
        context["skills"] = skills
        context["country"] = country
        context["city"] = city
        context["location"] = location
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)
    else:
        return render(request, "pages/experts/all_experts_search2.html", )


def expert_search_c_c_i(request, language, country, city):
    if request.POST:
        print('ditillaaqqq')
        context = {}
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        language = language
        country = country
        city = city
        language = language.replace("-", " ")
        country = country.replace("-", " ")
        city = city.replace("-", " ")
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(language__language__icontains=language) &
            Q(country__icontains=country) &
            Q(city__icontains=city)
        ).order_by("-id")
        context["experts"] = experts
        context["name"] = name
        context["language"] = language
        context["country"] = country
        context["city"] = city
        context["location"] = location
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)
    else:
        return render(request, "pages/experts/all_experts_search2.html", )


def expert_search_4(request, skills, language, country, city):
    if request.POST:
        context = {}
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        skills = skills
        language = language
        country = country
        city = city
        country = country.replace("-", " ")
        skills = skills.replace("-", " ")
        language = language.replace("-", " ")
        city = city.replace("-", " ")
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(fields_of_experties__expertise_fields=skills) &
            Q(language__language__icontains=language) &
            Q(country__icontains=country) &
            Q(city__icontains=city)
        ).order_by("-id")
        context["experts"] = experts
        context["name"] = name
        context["skills"] = skills
        context["language"] = language
        context["country"] = country
        context["city"] = city
        context["location"] = location
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)
    else:
        return render(request, "pages/experts/all_experts_search2.html", )


def expert_search_i_c_c(request, skills, language, country, ):
    if request.POST:
        print("duz yoldasan")
        context = {}
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        skills = skills
        language = language
        country = country
        country = country.replace("-", " ")
        skills = skills.replace("-", " ")
        language = language.replace("-", " ")
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(fields_of_experties__expertise_fields=skills) &
            Q(language__language__icontains=language) &
            Q(country__icontains=country)
        ).order_by("-id")
        context["experts"] = experts
        context["name"] = name
        context["skills"] = skills
        context["language"] = language
        context["country"] = country
        context["location"] = location
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)
    else:
        return render(request, "pages/experts/all_experts_search2.html", )


def expert_search_ind_country(request, skills, country, ):
    if request.POST:
        context = {}
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        skills = skills
        country = country
        country = country.replace("-", " ")
        skills = skills.replace("-", " ")
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(fields_of_experties__expertise_fields=skills) &
            Q(country__icontains=country)
        ).order_by("-id")
        context["experts"] = experts
        context["name"] = name
        context["skills"] = skills
        context["country"] = country
        context["location"] = location
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)
    else:
        return render(request, "pages/experts/all_experts_search2.html", )


def expert_search_comp_country(request, language, country, ):
    if request.POST:
        context = {}
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        language = language
        country = country
        language = language.replace("-", " ")
        country = country.replace("-", " ")
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(language__language__icontains=language) &
            Q(country__icontains=country)
        ).order_by("-id")
        context["experts"] = experts
        context["name"] = name
        context["language"] = language
        context["country"] = country
        context["location"] = location
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)
    else:
        return render(request, "pages/experts/all_experts_search2.html", )


def expert_search_ind_comp(request, skills, language, ):
    if request.POST:
        print('sanity_check 3')
        context = {}
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        language = language
        skills = skills
        language = language.replace("-", " ")
        skills = skills.replace("-", " ")
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(language__language__icontains=language) &
            Q(fields_of_experties__expertise_fields=skills)
        ).order_by("-id")
        context["experts"] = experts
        context["name"] = name
        context["language"] = language
        context["skills"] = skills
        context["location"] = location
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)
    else:
        return render(request, "pages/experts/all_experts_search2.html", )


def expert_search_ind(request, skills, ):
    if request.POST:
        context = {}
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        skills = skills
        skills = skills.replace("-", " ")
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(fields_of_experties__expertise_fields=skills)
        ).order_by("-id")
        context["experts"] = experts
        context["name"] = name
        context["skills"] = skills
        context["location"] = location
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)
    else:
        context = {}
        skills = skills
        skills = skills.replace("-", " ")
        experts = Expert.objects.filter(
            Q(fields_of_experties__expertise_fields=skills)
        ).order_by("-id")
        context["experts"] = experts
        context["skills"] = skills
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)


def expert_search_comp(request, language, ):
    if request.POST:
        context = {}
        name = request.POST.get('main-search')
        location = request.POST.get('location')
        language = language
        language = language.replace("-", " ")
        experts = Expert.objects.filter(
            Q(name__icontains=name) &
            Q(language__language__icontains=language)
        ).order_by("-id")
        context["experts"] = experts
        context["name"] = name
        context["language"] = language
        context["location"] = location
        context["expert_active"] = "menu-active"
        return render(request, "pages/experts/all_experts_search2.html", context)
    else:
        return render(request, "pages/experts/all_experts_search2.html", )


class NewExpertView(BaseContext, TemplateView):
    template_name = "pages/experts/add_expert.html"

    def get_context_data(self, **kwargs):
        context = super(NewExpertView, self).get_context_data(**kwargs)
        context["companies"] = Company.objects.all()
        context["industries"] = Industries.objects.all()
        context["expert_active"] = "menu-active"
        return context


def ac_search_e_name(request):
    print('sasaasa')
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Expert.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.name)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def ac_search_e_industry(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Industries.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.name)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def ac_search_e_company(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Company.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.name)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def ac_search_e_skills(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = ExpertTags1.objects.filter(expertise_fields__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.expertise_fields)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)


def ac_search_e_lang(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Languages.objects.filter(language__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.language)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def linkedin_auth(request):
    if request.GET:
        if Expert.objects.filter(slug=request.GET['state']).exists():
            code = request.GET['code']
            slug = request.GET['state']
            url = 'https://www.linkedin.com/oauth/v2/accessToken'
            params = {
                'client_id': settings.CLIENT_ID,
                'grant_type': 'authorization_code',
                'redirect_uri': settings.REDIRECT_URI,
                'code': code,
                'client_secret': settings.CLIENT_SECRET,
            }
            response = requests.post(url, params=params)
            if response.status_code == 200:
                response = response.json()
                auth_token = response['access_token']
                print(auth_token)
                header = {'Authorization': 'Bearer ' + auth_token}
                url = 'https://api.linkedin.com/v2/me'
                response = requests.get(url, headers=header, )
                if response.status_code == 200:
                    response = response.json()
                    expert = Expert.objects.get(slug=slug)
                    # TODO gelecekde id elde edilerse id-ye gore yoxlama aparilacaq
                    linkedin_name = response['localizedFirstName'] + ' ' + response['localizedLastName']
                    if expert.name == linkedin_name:
                        Expert.objects.filter(slug=slug).update(claimed=True)
                        return HttpResponse("Profile successfully claimed")
                    else:
                        return HttpResponse("Accounts didn't match!")

                else:
                    return HttpResponse(response.text)
            else:
                return HttpResponse(response.text)
        else:
            return HttpResponse("Requested account not found!")


class ExpertFollowAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = Expert.objects.get(slug=slug)
        user = self.request.user

        updated = False
        followed = False
        if user.is_authenticated:
            user1 = UserProfileModel.objects.get(user=user)
            if user1 in obj.follower_list.all():
                followed = False
                obj.follower_list.remove(user1)
            else:
                followed = True
                obj.follower_list.add(user1)

            updated = True

        data = {
            "updated": updated,
            "followed": followed
        }

        return Response(data)


class EventViewSet(APIView):

    @classmethod
    def get_extra_actions(cls):
        return []

    def get(self, request, **kwargs):
        if ExpertEvents.objects.filter(expert__slug=self.kwargs['slug']):
            queryset = ExpertEvents.objects.filter(
                expert__slug=self.kwargs['slug']
            ).filter(
                event__start_event_dt__lt=datetime.today()
            )
            serializer = ExpertEventSerializer(queryset, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Not Found!', status=status.HTTP_404_NOT_FOUND)


class ExpertAccountStatus(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, **kwargs, ):
        if Expert.objects.filter(slug=self.kwargs['slug']):
            claimed = Expert.objects.get(slug=self.kwargs['slug']).claimed
            data = {
                "claimed": claimed
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response('Requested Account Not Found')


def expert_profile_meter(slug):
    expert = Expert.objects.get(slug=slug)
    ExpertProfileCompilation.objects.filter(expert=expert).delete()
    counter = 0
    ExpertProfileCompilation.objects.create(expert=expert, name='Company')
    ExpertProfileCompilation.objects.create(expert=expert, name='Location')
    ExpertProfileCompilation.objects.create(expert=expert, name='Skills')
    ExpertProfileCompilation.objects.create(expert=expert, name='Business Title')
    ExpertProfileCompilation.objects.create(expert=expert, name='Bio')
    ExpertProfileCompilation.objects.create(expert=expert, name='Profile Picture')
    ExpertProfileCompilation.objects.create(expert=expert, name='Contact')
    ExpertProfileCompilation.objects.create(expert=expert, name='Age')
    ExpertProfileCompilation.objects.create(expert=expert, name='Social Profile Links')
    if expert.company.exists():
        ExpertProfileCompilation.objects.filter(expert=expert, name='Company').update(icon_url="completed.png")
        counter += 1
    if expert.location:
        ExpertProfileCompilation.objects.filter(expert=expert, name='Location').update(icon_url="completed.png")
        counter += 1
    if expert.fields_of_experties.exists():
        ExpertProfileCompilation.objects.filter(expert=expert, name='Skills').update(icon_url="completed.png")
        counter += 1
    if expert.business_title:
        ExpertProfileCompilation.objects.filter(expert=expert, name='Business Title').update(icon_url="completed.png")
        counter += 1
    if expert.bio:
        ExpertProfileCompilation.objects.filter(expert=expert, name='Bio').update(icon_url="completed.png")
        counter += 1
    if expert.expert_img:
        ExpertProfileCompilation.objects.filter(expert=expert, name='Profile Picture').update(icon_url="completed.png")
        counter += 1
    if expert.contact:
        ExpertProfileCompilation.objects.filter(expert=expert, name='Contact').update(icon_url="completed.png")
        counter += 1
    if expert.age:
        ExpertProfileCompilation.objects.filter(expert=expert, name='Age').update(icon_url="completed.png")
        counter += 1
    if expert.facebook_url or expert.linkedin_url or expert.twitter_url or expert.personal_url:
        ExpertProfileCompilation.objects.filter(expert=expert, name='Social Profile Links') \
            .update(icon_url="completed.png")
        counter += 1

    p = counter / 6 * 100
    p = round(p, 0)
    Expert.objects.filter(slug=slug).update(completion_percentage=p)
    Expert.objects.filter(slug=slug).update(et_points=expert.avg_rating * 20 * expert.completion_percentage / 100)


class ExpertProfileView(ExpertRequiredMixin, BaseContext, DetailView, ):
    model = Expert
    template_name = 'pages/profiles/expert/expert_profile.html'
    context_object_name = 'expert'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(ExpertProfileView, self).get_context_data(**kwargs)
        if Expert.objects.get(slug=self.kwargs['slug']).user:
            user_profile = UserProfileModel.objects.get(user=Expert.objects.get(slug=self.kwargs['slug']).user)
            context["following_events"] = Event.objects.filter(
                follower_list=user_profile
            )
            context["following_experts"] = Expert.objects.filter(
                follower_list=user_profile
            )
            context["following_companies"] = Company.objects.filter(
                follower_list=user_profile
            )
            # Recommended events based on following events
            cat_list = []
            event_list = []
            for event in user_profile.followed_events.all():
                event_list.append(event.pk)
                for cat in event.category.all():
                    cat_list.append(cat)
            context["recommended_events"] = Event.objects.filter(category__in=cat_list).exclude(pk__in=event_list)[:6]

        context["dashboard_active"] = "active"
        # context["expert_follow"] = "Follow"
        # Profile Stats - Profile Hits
        expert = Expert.objects.get(slug=self.kwargs['slug'])
        expert_id = Expert.objects.get(slug=self.kwargs['slug']).id
        content_type_id = ContentType.objects.get_for_model(expert).pk
        context["profile_compilation"] = ExpertProfileCompilation.objects.filter(expert=expert)
        if HitCount.objects.filter(content_type_id=content_type_id, object_pk=expert_id):
            period = datetime.now() - timedelta(days=7)
            hit_count_id = HitCount.objects.get(content_type_id=content_type_id, object_pk=expert_id).id
            hit = Hit.objects.filter(hitcount=hit_count_id, created__gt=period).annotate(
                month=ExtractDay('created')).values('month').annotate(c=Coalesce(Count('month'), 0)).order_by('month')
            hit2 = list(hit)
            days = []
            counts = []
            for row in hit2:
                days.append(row['month'])
                counts.append(row['c'])
            context["days"] = days
            context["counts"] = counts
            # base = datetime.today()
            # date_list = [base - timedelta(days=x) for x in range(7)]
        expert_profile_meter(self.kwargs['slug'])
        return context


class ExpertProfileEditView(ExpertRequiredMixin, BaseContext, DetailView):
    model = Expert
    template_name = 'pages/profiles/expert/expert_profile_edit.html'
    context_object_name = 'expert'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(ExpertProfileEditView, self).get_context_data(**kwargs)
        expert = Expert.objects.get(slug=self.kwargs['slug'])
        context["expert_events"] = ExpertEvents.objects.filter(
            expert=expert
        )
        context["event_tags"] = ExpertTags.objects.all()
        context["colleagues"] = ExpertColleagues.objects.filter(
            expert=expert
        )
        context["lang_levels"] = LanguageLevel.objects.all()
        context["languages"] = ExpertLanguages.objects.filter(expert=expert)
        # for menu active class frontend
        context["edit_active"] = "active"
        return context


# expert profile searc coll
def ac_search_e_name_col(request):
    print('ssss')
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Expert.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            expert = {}
            expert["id"] = r.pk
            expert["name"] = r.name
            expert["img"] = r.expert_img.url
            expert["slug"] = r.slug
            results.append(expert)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# class ExpertProfileMyEventView(ExpertRequiredMixin, BaseContext, DetailView):
#     model = Expert
#     template_name = 'pages/profiles/expert/expert_profile_event.html'
#     context_object_name = 'expert'
#     count_hit = True
#
#     def get_context_data(self, **kwargs):
#         context = super(ExpertProfileMyEventView, self).get_context_data(**kwargs)
#         if Expert.objects.get(slug=self.kwargs['slug']).user:
#             user_profile = UserProfileModel.objects.get(user=Expert.objects.get(slug=self.kwargs['slug']).user)
#             context["events"] = Event.objects.all()[:6]
#             context["experts"] = Expert.objects.all()[:3]
#             context["companies"] = Company.objects.first()
#
#         # for menu active class frontend
#         context["myevent_active"] = "active"
#         context["event_form"] = EventForm()
#         return context
#
#     def post(self, request, slug):
#         form = EventForm(request.POST)
#         self.event_form = form
#         print(form.errors)
#         if form.is_valid():
#             event = form.save()
#             return redirect('index_url')
#         return HttpResponseRedirect(reverse('expert_profile_myevent',
#                                     kwargs={'slug': slug}, ))


class ExpertProfileMyEventView(ExpertRequiredMixin, FormMixin, DetailView):
    template_name = 'pages/profiles/expert/expert_profile_event.html'
    model = Expert
    form_class = EventForm

    def get_success_url(self):
        return reverse('expert_profile_myevent', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(ExpertProfileMyEventView, self).get_context_data(**kwargs)
        if Expert.objects.get(slug=self.kwargs['slug']).user:
            user_profile = UserProfileModel.objects.get(user=Expert.objects.get(slug=self.kwargs['slug']).user)
            context["events"] = Event.objects.all()[:6]
            context["experts"] = Expert.objects.all()[:3]
            context["companies"] = Company.objects.first()
            context['event_form'] = EventForm(initial={'post': self.object})

            # for menu active class frontend
            context["myevent_active"] = "active"

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            instance = form.save()
            event = Event.objects.get(pk=instance.pk)
            # Adding Event tags
            if request.POST.get('ep-ce-tags'):
                tags = request.POST.get('ep-ce-tags')
                if tags[0] == ";":
                    tags = tags[1:]
                tags = tags.split(";")
                for i in tags:
                    tag = Tags.objects.get(
                        tag_name=i
                    )
                    event.tag.add(tag)
            # Adding Speakers
            if request.POST.get('exp_colls'):
                speakers = request.POST.get('exp_colls')
                if speakers[0] == ";":
                    speakers = speakers[1:]
                speakers = speakers.split(";")
                for i in speakers:
                    speakers = Expert.objects.get(
                        pk=i
                    )
                    ExpertEvents.objects.create(
                        event=event,
                        expert=speakers,
                    )
            # Adding Sponsors
            if request.POST.get('ep-ce-sponsors'):
                tags = request.POST.get('ep-ce-sponsors')
                if tags[0] == ";":
                    tags = tags[1:]
                tags = tags.split(";")
                for i in tags:
                    tag = EventSponsors.objects.get(
                        pk=i
                    )
                    event.sponsor.add(tag)
            # Adding Organizers
            if request.POST.get('ep-ce-org'):
                tags = request.POST.get('ep-ce-org')
                if tags[0] == ";":
                    tags = tags[1:]
                tags = tags.split(";")
                for i in tags:
                    tag = Organizer.objects.get(
                        pk=i
                    )
                    event.organizer.add(tag)
            if request.POST.get('ep-ce-ac-op'):
                event_obj = Event.objects.filter(pk=instance.pk)
                if request.POST.get('ep-ce-ac-op') == 'yes':
                    event_obj.update(speaker_submission=True)
                    event_obj.update(submission_details=request.POST.get('ep-ce-ac-desc'))
                if request.POST.get('ep-ce-acs-receive-type') == 'yes':
                    event_obj.update(application_type=True)
                else:
                    event_obj.update(application_type=False)
                    event_obj.update(submission_web_site=request.POST.get('ep-ce-acs-receive-address'))
            if request.POST.get('ep-ce-pt-list'):
                input_values = request.POST.get('ep-ce-pt-list')
                if input_values[0] == ";":
                    input_values = input_values[1:]
                input_values = input_values.split(";")
                for name in input_values:
                    Ticket.objects.create(
                        event=event,
                        name=request.POST.get('ep-ce-pt-' + name + '-title'),
                        price=request.POST.get('ep-ce-pt-' + name + '-price'),
                    )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # form.save()
        return super(ExpertProfileMyEventView, self).form_valid(form)


class ExpertUpdateProfile(ExpertRequiredMixin, View):
    def post(self, request, slug):
        curid = 111
        tag = 'exp-event-atendee-type' + str(curid)
        Expert.objects.filter(slug=slug).update(
            # TODO needs to validate data
            name=request.POST.get('exp_fullname'),
            location=request.POST.get('exp_location'),
            slug=request.POST.get('exp_pub_url'),
            business_title=request.POST.get('exp_title'),
            bio=request.POST.get('exp-bio'),
            personal_url=request.POST.get('exp_web_link'),
            facebook_url=request.POST.get('exp_fb_link'),
            twitter_url=request.POST.get('exp_tw_link'),
            linkedin_url=request.POST.get('exp_ln_link'),
        )
        slug = request.POST.get('exp_pub_url')
        # Updating company
        expert = Expert.objects.get(slug=slug)
        old_companies = Company.objects.filter(expert__slug=slug)
        for company in old_companies:
            expert.company.remove(company)
        if request.POST.get('current_comp'):
            new_company = Company.objects.get(pk=request.POST.get('current_comp'))
            expert.company.add(new_company)
        # Updating expert skills
        old_skills = ExpertTags1.objects.filter(expert__slug=slug)
        for skill in old_skills:
            expert.fields_of_experties.remove(skill)
        print("SKILS *** GELUIO")
        print(request.POST.get('exp_skills'))
        if request.POST.get('exp_skills'):
            skills = request.POST.get('exp_skills')
            if skills[0] == ";":
                skills = skills[1:]
            skills = skills.split(";")
            for i in skills:
                tag = ExpertTags1.objects.get(
                    expertise_fields=i
                )
                expert.fields_of_experties.add(tag)
        # Updating events

        # Updating Colleagues
        ExpertColleagues.objects.filter(expert=expert).delete()
        if request.POST.get('exp_colls'):
            new_colls = request.POST.get('exp_colls')
            if new_colls[0] == ";":
                new_colls = new_colls[1:]
            new_colls = new_colls.split(";")
            for coll in new_colls:
                ExpertColleagues.objects.create(
                    expert=expert,
                    colleague=Expert.objects.get(pk=coll),
                )
        # Updating Languages
        ExpertLanguages.objects.filter(expert=expert).delete()
        if request.POST.get('ep-langs'):
            input_values = request.POST.get('ep-langs')
            if input_values[0] == ";":
                input_values = input_values[1:]
            input_values = input_values.split(";")
            for name in input_values:
                print(request.POST.get('ep-lang-' + name))
                ExpertLanguages.objects.create(
                    expert=expert,
                    language=Languages.objects.get(language=request.POST.get('ep-lang-' + name)),
                    level=LanguageLevel.objects.get(level=request.POST.get('lang-level-' + name)),
                )
        return redirect("expert_profile_edit", slug=slug)


class ImportExpertExcelList(APIView):
    def get(self, request, ):
        if request.user.is_superuser:
            return render(request, "pages/importexport/import_expert_crunchbase.html")
        else:
            return HttpResponseForbidden()

    def post(self, request, format=None):
        if request.user.is_superuser:
            try:
                excel_file = request.FILES['file']
            except MultiValueDictKeyError:
                return redirect('import_expert_excel_list')
            if str(excel_file).split('.')[-1] == "xls":
                data = xls_get(excel_file, column_limit=17)
            elif str(excel_file).split('.')[-1] == "xlsx":
                data = xlsx_get(excel_file, column_limit=17)
            else:
                return redirect('import_expert_excel_list')

            experts = data["experts"]

            if len(experts) > 1:  # We have expert data
                for expert in experts:
                    try:

                        expert_profile_pic_url = expert[0]
                        expert_name = expert[1]
                        expert_btitle = expert[2]
                        expert_company = expert[3]
                        expert_location = expert[4]
                        expert_regions = expert[5]
                        expert_gender = expert[6]
                        expert_bio = expert[7]
                        expert_investor_type = expert[8]
                        expert_investor_stage = expert[9]
                        expert_num_ex = expert[10]
                        expert_website = expert[11]
                        expert_facebook = expert[12]
                        expert_linkedin = expert[13]
                        expert_twitter = expert[14]

                        resp = requests.get(expert_profile_pic_url)

                        fp = BytesIO()
                        fp.write(resp.content)
                        file_name = ''
                        file_name = strip_accents(expert_name) + file_name
                        file_name = remove_special(file_name)
                        file_name = file_name.lower()

                        new_expert = Expert()
                        # new_expert.expert_img.save(new_file, files.File(fp))
                        new_expert.expert_img.save(file_name, files.File(fp))
                        new_expert.business_title = expert_btitle
                        new_expert.location = expert_location
                        new_expert.bio = expert_bio
                        if not expert_twitter == 'None':
                            new_expert.twitter_url = expert_twitter
                        if not expert_linkedin == 'None':
                            new_expert.linkedin_url = expert_linkedin
                        if not expert_facebook == 'None':
                            new_expert.facebook_url = expert_facebook
                        new_expert.personal_url = expert_website
                        new_expert.is_approved = True
                        new_expert.name = expert_name
                        new_expert.save_2()
                        print(expert_name)
                    except:
                        traceback.print_exc()
                        continue

            return redirect('import_expert_excel_list')
        else:
            return HttpResponseForbidden()
