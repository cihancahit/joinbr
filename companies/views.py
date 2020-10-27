from datetime import datetime, timedelta
import json as json2

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView, DetailView, ListView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from companies.models import *
from events.models import Event
from expert.models import Expert, ExpertEvents, ExpertTags
from fec_app.views import BaseContext
from reviews_and_rating.forms import ReviewForm
from reviews_and_rating.models import ReviewModel
from users.models import UserProfileModel
from custom.custom_tools2 import get_user
from hitcount.views import HitCountDetailView

import requests
import random
import string
from bs4 import BeautifulSoup
from django.core import files
from io import BytesIO

from companies.models import Company, Markets, CompanyAddress
from custom.custom_tools2 import is_int, slugify
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
import traceback


class CompanyView(BaseContext, ListView):
    template_name = "pages/companies/all_companies2.html"
    context_object_name = "companies"
    paginate_by = 10
    sort_type = 'alphabetic-asc'
    filter_type = '*'
    company_list1 = {}

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        if self.request.GET.get('paginate_by'):
            self.request.session['pagec'] = self.request.GET.get('paginate_by')
        else:
            self.request.session['pagec'] = self.paginate_by
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        if self.request.GET.get('sort'):
            self.sort_type = self.request.GET.get('sort')

        company_list = Company.objects.all()

        if self.sort_type == 'relevancy':
            # TODO relevancy will be added
            company_list = company_list.order_by("-id")
        elif self.sort_type == 'alphabetic-asc':
            company_list = company_list.order_by("name")
        elif self.sort_type == 'alphabetic-desc':
            company_list = company_list.order_by("-name")
        elif self.sort_type == 'popularity':
            # TODO popularity will be added
            company_list = company_list.order_by("id")
        else:
            company_list = company_list.order_by("-id")

        self.company_list1 = company_list
        return company_list

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        context["reviews"] = 1
        period = datetime.now() - timedelta(days=7)
        context["popular_experts"] = Expert.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:4]
        context["popular_events"] = Event.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:4]
        # context["companies"] = Company.objects.annotate(
        #     score_count=Count('reviewmodel')
        # ).order_by('-id')
        context["company_active"] = "menu-active"
        context["company_count"] = self.company_list1.count()
        if self.request.session.get('pagec'):
            context["pagec"] = self.request.session.get('pagec')

        context["sort_type"] = self.request.session['sort_type'] = self.sort_type
        context["markets"] = Markets.objects.all()

        return context


@login_required
def company_list(request):
    companies = Company.objects.annotate(
        score_count=Count('reviewmodel')
    ).values('company_logo', 'name', 'location', 'city', 'founded', 'markets', 'avg_rating', ).order_by('-id')
    company_lists = list(companies)

    return JsonResponse(company_lists, safe=False)


class CompanyDetailView(BaseContext, HitCountDetailView):
    model = Company
    template_name = 'pages/companies/company_detail2.html'
    context_object_name = 'company'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        company = Company.objects.get(slug=slug)
        review_count = ReviewModel.objects.filter(company__slug=slug).count()
        context["reviews"] = ReviewModel.objects.filter(company__slug=slug)
        context["experts"] = Expert.objects.get_queryset().filter(company__slug=self.kwargs['slug'])[:3]
        context["products"] = CompanyProduct.objects.get_queryset().filter(company=company)[:5]
        context["product_count"] = CompanyProduct.objects.get_queryset().filter(company=company).count()
        context["review_form"] = ReviewForm
        context["reviews_count"] = review_count
        context["company_active"] = "menu-active"
        context["loggeduser"] = self.request.user
        context["date"] = datetime.today()
        # context["follower_count"] = Users.
        # if RatingModel.objects.filter(reviewed_item=company).exists():
        #     context["excellent"] = str(round(RatingModel.objects.get(
        #         reviewed_item=company).excellent / review_count * 100)) + '%'
        #     context["great"] = str(round(RatingModel.objects.get(
        #         reviewed_item=company).great / review_count * 100)) + '%'
        #     context["average"] = str(round(RatingModel.objects.get(
        #         reviewed_item=company).average / review_count * 100)) + '%'
        #     context["poor"] = str(round(RatingModel.objects.get(
        #         reviewed_item=company).poor / review_count * 100)) + '%'
        #     context["bad"] = str(round(RatingModel.objects.get(
        #         reviewed_item=company).bad / review_count * 100)) + '%'
        context["logged_user"] = get_user(self.request)
        if company.location.count() > 0:
            address = company.location.all()
            addr = address.get(is_primary=True)
            main_address = ''
            if addr.city is not None:
                main_address = addr.city
            elif addr.country is not None:
                main_address = main_address + ', ' + addr.country
            context['main_address'] = main_address
        else:
            context['main_address'] = 'Address Not Specified'

        if ExpertEvents.objects.filter(expert__slug=self.kwargs['slug']):
            context["events_f"] = ExpertEvents.objects.filter(expert__slug=self.kwargs['slug']).filter(
                event__start_event_dt__gt=datetime.today())[:3]
        context["other_comp"] = Company.objects.all()[:6]
        context['reviewer_tags'] = ExpertTags.objects.all()
        context['meta'] = self.get_object().as_meta(self.request)

        return context


class CompanySearchView(BaseContext, ListView):
    template_name = "pages/companies/all_companies_search.html"

    def get(self, request, *args, **kwargs, ):
        context = {}
        name = request.GET.get('company_name')
        company_type = request.GET.get('type')
        city = request.GET.get('city')
        country = request.GET.get('country')
        companies = Company.objects.filter(
            Q(name__icontains=name) &
            Q(type__name__icontains=company_type) &
            Q(location__icontains=city) &
            Q(city__icontains=country)
        ).order_by("-id")
        context["companies"] = companies
        context["name"] = name
        context["type"] = company_type
        context["city"] = city
        context["country"] = country
        context["company_active"] = "menu-active"

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs, ):
        context = {}
        name = request.POST.get('company_name')
        companies = Company.objects.filter(
            Q(name__icontains=name))
        context["companies"] = companies
        context["name"] = name
        context["company_active"] = "menu-active"
        period = datetime.now() - timedelta(days=7)
        context["popular_experts"] = Expert.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:4]
        context["popular_events"] = Event.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:4]
        context["markets"] = Markets.objects.all()

        return render(request, self.template_name, context)


def company_search_3(request, market, country, city):
    if request.POST:
        context = {}
        name = request.POST.get('company_name')
        company_type = market
        city = city
        country = country
        company_type = company_type.replace("-", " ")
        city = city.replace("-", " ")
        country = country.replace("-", " ")
        companies = Company.objects.filter(
            Q(name__icontains=name) &
            Q(type__name__icontains=company_type) &  # markets__market_name__icontains
            Q(location__icontains=country) &
            Q(city__icontains=city)
        ).order_by("-id")
        context["companies"] = companies
        context["name"] = name
        context["type"] = company_type
        context["city"] = city
        context["country"] = country
        context["company_active"] = "menu-active"
        return render(request, "pages/companies/all_companies_search.html", context)
    else:
        return render(request, "pages/companies/all_companies_search.html", )


def company_search_market(request, market, ):
    if request.POST:
        context = {}
        name = request.POST.get('company_name')
        company_type = market
        company_type = company_type.replace("-", " ")
        companies = Company.objects.filter(
            Q(name__icontains=name) &
            Q(markets__market_name__icontains=company_type)
        ).order_by("-id")
        context["companies"] = companies
        context["name"] = name
        context["inq_market"] = company_type
        context["company_active"] = "menu-active"
        period = datetime.now() - timedelta(days=7)
        context["popular_experts"] = Expert.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:4]
        context["popular_events"] = Event.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:4]
        context["markets"] = Markets.objects.all()
        return render(request, "pages/companies/all_companies_search.html", context)
    else:
        return render(request, "pages/companies/all_companies_search.html", )


def company_search_country(request, location, ):
    if request.POST:
        context = {}
        name = request.POST.get('company_name')
        location = location.replace("-", " ")
        address = CompanyAddress.objects.filter(
            Q(city__icontains=location) |
            Q(location__icontains=location) |
            Q(country__icontains=location)
        )
        companies = Company.objects.filter(
            Q(name__icontains=name) &
            Q(location__in=address)
        ).order_by("-id")
        context["companies"] = companies
        context["name"] = name
        context["location"] = location
        context["company_active"] = "menu-active"
        period = datetime.now() - timedelta(days=7)
        context["popular_experts"] = Expert.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:4]
        context["popular_events"] = Event.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:4]
        context["markets"] = Markets.objects.all()
        return render(request, "pages/companies/all_companies_search.html", context)
    else:
        return render(request, "pages/companies/all_companies_search.html", )


def company_search_city(request, country, city):
    if request.POST:
        context = {}
        name = request.POST.get('company_name')
        country = country
        city = city
        country = country.replace("-", " ")
        city = city.replace("-", " ")
        companies = Company.objects.filter(
            Q(name__icontains=name) &
            Q(location__icontains=country) &
            Q(city__icontains=city)
        ).order_by("-id")
        context["companies"] = companies
        context["name"] = name
        context["country"] = country
        context["city"] = city
        context["company_active"] = "menu-active"
        return render(request, "pages/companies/all_companies_search.html", context)
    else:
        return render(request, "pages/companies/all_companies_search.html", )


def company_search_market_country(request, market, location):
    if request.POST:
        context = {}
        name = request.POST.get('company_name')
        company_type = market
        company_type = company_type.replace("-", " ")
        location = location.replace("-", " ")
        address = CompanyAddress.objects.filter(
            Q(city__icontains=location) |
            Q(location__icontains=location) |
            Q(country__icontains=location)
        )
        companies = Company.objects.filter(
            Q(name__icontains=name) &
            Q(markets__market_name__icontains=company_type) &
            Q(location__in=address)
        ).order_by("-id")
        context["companies"] = companies
        context["name"] = name
        context["location"] = location
        context["inq_market"] = company_type
        context["company_active"] = "menu-active"
        period = datetime.now() - timedelta(days=7)
        context["popular_experts"] = Expert.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:4]
        context["popular_events"] = Event.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:4]
        context["markets"] = Markets.objects.all()
        return render(request, "pages/companies/all_companies_search.html", context)
    else:
        return render(request, "pages/companies/all_companies_search.html", )


# Ajax search input autocomplete


def ac_search_c_name(request):
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


def ac_search_c_market(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Markets.objects.filter(market_name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.market_name)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


class CompanyFollowAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = Company.objects.get(slug=slug)

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


# expert profile searc company
def ac_search_c_name_profile(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Company.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            company = {}
            company["id"] = r.pk
            # ddkifnsdndn
            company["name"] = r.name
            company["img"] = r.company_logo.url
            results.append(company)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


class CompanyProfileEditView(BaseContext, DetailView):
    model = Company
    template_name = 'pages/profiles/company/company_profile_edit.html'
    context_object_name = 'company'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(CompanyProfileEditView, self).get_context_data(**kwargs)
        expert = Company.objects.get(slug=self.kwargs['slug'])
        # for menu active class frontend
        context["edit_active"] = "active"
        return context


class NewCompanyView(BaseContext, TemplateView):
    template_name = "pages/companies/add_company.html"

    def get_context_data(self, **kwargs):
        context = super(NewCompanyView, self).get_context_data(**kwargs)
        context["company_types"] = CompanyTypes.objects.all()
        context["company_active"] = "menu-active"
        return context


def add_company(request):
    if request.method == "POST":
        name = request.POST.get('name')
        info = request.POST.get('info')
        founded = request.POST.get('founded')
        website = request.POST.get('website')
        linkedin_url = request.POST.get('linkedin')
        facebook_url = request.POST.get('facebook')
        twitter_url = request.POST.get('twitter')
        startup = request.POST.get('startup')
        size = request.POST.get('size')
        ctype = request.POST.get('ctype')
        location = request.POST.get('address')
        if startup == 'startup':
            startup = True
        else:
            startup = False

        company = Company.objects.create(
            name=name,
            info=info,
            founded=founded,
            website=website,
            linkedin_url=linkedin_url,
            facebook_url=facebook_url,
            twitter_url=twitter_url,
            startup=startup,
            size=size,
            company_logo=request.FILES.get('file'),
            user=request.user,
        )

        company.type.add(CompanyTypes.objects.get(name=ctype))

        address1 = CompanyAddress.objects.create(location=location)
        company.location.add(address1)
        company.save()

        response_data = {'result': 'Create post successful!', }

        return HttpResponse(
            json2.dumps(response_data),
            content_type="application/json"
        )


def scrape_company_crunchabase(url):
    session = requests.Session()
    session.headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}

    # url = 'https://www.crunchbase.com/organization/zoom-video-communications'
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for i in range(8))
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, "html.parser")
    general_info = soup.find('image-with-fields-card')
    company_name_cont = general_info.find('blob-formatter')
    company_name = company_name_cont.find('span').text
    company_info_cont1 = soup.find('fields-card')
    company_info_cont = company_info_cont1.find('div')
    company_infos = company_info_cont.findChildren('span', recursive=False)
    i = 1
    company_info_dict = {}
    for company_info in company_infos:
        if i % 2 == 1:
            company_info_label = company_info.text
        else:
            company_info_value = company_info.text
            company_info_dict[company_info_label] = company_info_value
        i = i + 1
    try:
        company_info_soc_cont1 = soup.findAll('fields-card')[2:3]
        company_info_soc_cont = company_info_soc_cont1[0].find('div')
        company_info_social1 = company_info_soc_cont.findChildren('span', recursive=False)
        j = 1
        for company_info_social in company_info_social1:
            if j % 2 == 1:
                company_info_soc_label = company_info_social.text
            else:
                if company_info_soc_label == 'Facebook\xa0' or company_info_soc_label == 'LinkedIn\xa0' or company_info_soc_label == 'Twitter\xa0':
                    company_info_soc_value = company_info_social.find('a', href=True)
                    company_info_soc_value = company_info_soc_value['href']
                else:
                    company_info_soc_value = company_info_social.text

                company_info_dict[company_info_soc_label] = company_info_soc_value
            j = j + 1
    except:
        print('salam')

    try:
        desc_card = soup.find('description-card')
        company_desc = desc_card.findAll('p')[0].text
    except:
        company_desc = ''

    try:
        company_desc = company_desc + desc_card.findAll('p')[1].text
    except:
        company_desc = company_desc

    if 'Website\xa0' in company_info_dict:
        img_src = 'http://logo.clearbit.com/' + company_info_dict['Website\xa0']
        resp = requests.get(img_src)
        fp = BytesIO()
        fp.write(resp.content)
        file_name = slugify(company_name + random_str)
        # print(slugify(company_name+random_str))
    new_company = Company()

    if 'Website\xa0' in company_info_dict:
        new_company.company_logo.save(file_name, files.File(fp))
    if company_name is not None:
        new_company.name = company_name
    if company_desc is not None:
        new_company.info = company_desc
    if 'Website\xa0' in company_info_dict:
        new_company.website = company_info_dict['Website\xa0']
    if 'Founded Date\xa0' in company_info_dict:
        if is_int(company_info_dict['Founded Date\xa0']):
            new_company.founded = company_info_dict['Founded Date\xa0']
    if 'Number of Employees\xa0' in company_info_dict:
        employee_count = company_info_dict['Number of Employees\xa0'].split('-')[-1]
        if is_int(int(employee_count)):
            new_company.size = int(employee_count)
    if 'Facebook\xa0' in company_info_dict:
        new_company.facebook_url = company_info_dict['Facebook\xa0']
    if 'LinkedIn\xa0' in company_info_dict:
        new_company.linkedin_url = company_info_dict['LinkedIn\xa0']
    if 'Twitter\xa0' in company_info_dict:
        new_company.twitter_url = company_info_dict['Twitter\xa0']
    if 'Contact Email\xa0' in company_info_dict:
        new_company.contact_email = company_info_dict['Contact Email\xa0']
    if 'Phone Number\xa0' in company_info_dict:
        new_company.contact_number = company_info_dict['Phone Number\xa0']
    # new_company.slug = slugify(company_name+random_str)

    new_company.save()
    new_loc = CompanyAddress()
    if 'Headquarters Regions\xa0' in company_info_dict:
        # location = company_info_dict['Headquarters Regions\xa0'].split(',')
        new_loc = CompanyAddress()
        new_loc.location = company_info_dict['Headquarters Regions\xa0']
        new_loc.save()

    new_company.location.add(new_loc)
    if 'Industries\xa0' in company_info_dict:
        catexp = company_info_dict['Industries\xa0'].split(',')

        for market_name in catexp:
            new_market = Markets()
            if Markets.objects.filter(market_name=market_name).exists():
                new_company.markets.add(Markets.objects.get(market_name=market_name))
            else:
                new_market.market_name = market_name
                new_market.save()
                new_company.markets.add(new_market)


class ImportCompanyExcelList(APIView):
    def get(self, request, ):
        if request.user.is_superuser:
            return render(request, "pages/importexport/import_company_crunchbase.html")
        else:
            return HttpResponseForbidden()

    def post(self, request, format=None):
        if request.user.is_superuser:
            try:
                excel_file = request.FILES['file']
            except MultiValueDictKeyError:
                return redirect('import_company_excel_list')
            if str(excel_file).split('.')[-1] == "xls":
                data = xls_get(excel_file, column_limit=28)
            elif str(excel_file).split('.')[-1] == "xlsx":
                data = xlsx_get(excel_file, column_limit=28)
            else:
                return redirect('import_company')

            companies = data["companies"]

            if len(companies) > 1:  # We have company data
                for company in companies:
                    try:
                        company_logo_url = company[0]
                        company_name = company[1]
                        company_short_desc = company[2]
                        company_loc = company[3]
                        company_desc = company[4]
                        company_ind = company[5]
                        company_headq = company[6]
                        company_founded = company[7]
                        company_founders = company[8]
                        company_op_status = company[9]
                        company_nofemployee = company[10]
                        company_child_hub = company[11]
                        company_invest_type = company[12]
                        company_invest_stage = company[13]
                        company_n_e = company[14]
                        company_website = company[15]
                        company_facebook = company[16]
                        company_linkedin = company[17]
                        company_twitter = company[18]
                        company_contact_email = company[19]
                        company_phone = company[20]
                        company_fund_status = company[21]
                        company_last_fund_status = company[22]
                        company_legal_name = company[23]
                        company_ipo_status = company[24]
                        company_comp_type = company[25]
                        company_also_known_as = company[26]
                        company_hub_tags = company[27]
                        # company_sub_org = company[28]

                        resp = requests.get(company_logo_url)

                        fp = BytesIO()
                        fp.write(resp.content)
                        file_name = ''
                        file_name = strip_accents(company_name) + file_name
                        file_name = remove_special(file_name)
                        file_name = file_name.lower()
                        new_company = Company()

                        new_company.company_logo.save(file_name, files.File(fp))
                        if company_name !='None':
                            new_company.name = company_name
                        if company_desc !='None':
                            new_company.info = company_desc
                        if company_short_desc !='None':
                            new_company.single_info = company_short_desc
                        if company_website != 'None':
                            if 'http' not in company_website:
                                new_company.website = 'http://'+company_website
                            else:
                                new_company.website = company_website
                        if company_facebook != 'None':
                            new_company.facebook_url = company_facebook
                        if company_linkedin != 'None':
                            new_company.linkedin_url = company_linkedin
                        if company_twitter != 'None':
                            new_company.twitter_url = company_twitter
                        if company_founded != 'None':
                            if is_int(company_founded):
                                new_company.founded = company_founded
                        if company_nofemployee != 'None':
                            employee_count = company_nofemployee.split('-')[-1]
                            if is_int(employee_count):
                                new_company.size = int(employee_count)
                        if company_contact_email != 'None':
                            new_company.contact_email = company_contact_email
                        if company_phone != 'None':
                            new_company.contact_number = company_phone

                        if company_loc !='None':
                            new_company.save()
                            new_loc = CompanyAddress()

                            new_loc = CompanyAddress()
                            new_loc.location = company_loc
                            new_loc.is_primary = True
                            new_loc.save()

                            new_company.location.add(new_loc)
                        if company_ind != 'None':
                            catexp = company_ind.split(',')
                            for market_name in catexp:
                                new_market = Markets()
                                if Markets.objects.filter(market_name=market_name).exists():
                                    new_company.markets.add(Markets.objects.get(market_name=market_name))
                                else:
                                    new_market.market_name = market_name
                                    new_market.save()
                                    new_company.markets.add(new_market)
                    except:
                        traceback.print_exc()
                        continue
            return redirect('import_company_excel_list')
        else:
            return HttpResponseForbidden()
