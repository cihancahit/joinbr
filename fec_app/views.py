import json as json2
from datetime import datetime, timedelta

from cities_light.models import Country, City
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import requests
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, render_to_response, redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.defaults import page_not_found
from rest_framework.views import APIView

from companies.models import Company, random_premium_company, Markets, CompanyTypes, CompanyAddress
from events.forms import EventForm
from events.models import Event, Category, random_premium_event
from expert.models import Expert, ExpertTags1, Industries, Availability
from fec_app.models import EmailList, Languages
from users.models import UserProfileModel
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from custom.custom_tools import getUserCity
from django.conf import settings


class BaseContext(View):
    def get_context_data(self, **kwargs):
        context = super(BaseContext, self).get_context_data(**kwargs)
        form = EventForm()
        login_form = AuthenticationForm()
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        if settings.DEBUG:
            ip = '137.26.23.120'
        context["city"] = getUserCity(ip)
        context["form"] = form
        context["login_form"] = login_form
        # TODO
        #  1. modal loginde eger melumatlar sehv post olunursa modalda bu haqda bildiris gosterilsin,
        #   hal hazirda redirect edir login forma
        #  2. hansi pagede modal acilibsa o pageden davam etsin
        return context


class IndexView(BaseContext, TemplateView):
    template_name = "pages/home1.html"

    def get_context_data(self, **kwargs):
        period = datetime.now() - timedelta(days=1)
        context = super(IndexView, self).get_context_data(**kwargs)
        context["events"] = Event.objects.all().order_by("-id")[:6]
        context["more_events"] = Event.objects.all().order_by("-id")[6:][:6]
        context["categories"] = Category.objects.all()[:16]  # TODO  will be retrieved with hitcount
        context["home_active"] = "menu-active"
        context["popular_events"] = Event.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:2]
        context["premium_events"] = random_premium_event()
        context["popular_experts"] = Expert.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:4]
        context["more_popular_experts"] = Expert.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[4:][:4]
        context["popular_companies"] = Company.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:2]
        context["premium_companies"] = random_premium_company()
        context["featured_event"] = Event.objects.filter(featured=True)[:1]

        user = self.request.user
        if user.is_authenticated:
            user1 = UserProfileModel.objects.get(user=user)
            context["logged_user"] = user1
        else:
            context["logged_user"] = "anonymous"
        return context


class EventDetailView(BaseContext, TemplateView):
    template_name = "pages/events/event_detail.html"

    def get(self, request, *args, **kwargs):
        context = {'path': 'event-detail'}
        return render(request, self.template_name, context=context)


def ac_search_c_country(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Country.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.name)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def ac_search_c_city(request):
    if request.is_ajax():
        q = request.GET.get('city', '').capitalize()
        country = request.GET.get('country')
        id = Country.objects.filter(name=country)
        search_qs = City.objects.filter(name__startswith=q, country=id[0])
        results = []
        for r in search_qs:
            results.append(r.name)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def comingSoon(request):
    template_name = "pages/cc.html"
    context = {}
    return render(request, template_name, context=context)


def is_human(captcha_response):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    secret = "6LepV88UAAAAAAHKfalmtMtEOTDq2SB7l90xj4ja"
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json2.loads(response.text)
    return response_text['success']


def emailSubmit(request):
    redirect_url = '/cc/'
    if request.method == 'POST':
        email = request.POST.get('email')
        email_update = request.POST.get('email-updates')
        checkemail = EmailList.objects.filter(email=email).count()
        g_token = request.POST.get('_token')
        if not is_human(g_token):
            messages.add_message(request, messages.ERROR, 'Hmm, I think you are bot.')
        else:
            if len(email) == 0:
                messages.add_message(request, messages.ERROR, 'Email can\'t be empty!')
            elif checkemail > 0:
                messages.add_message(request, messages.ERROR, 'We are already reviewing your inquiry!')
            else:
                emaillist = EmailList()
                emaillist.email = email
                if email_update:
                    emaillist.email_updates = True
                emaillist.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Thank you for your inquiry, bro/sis.<br/> We are currently reviewing applications for our private beta.<br/> As soon as your application is approved you will receive an email update from us.')
    else:
        messages.add_message(request, messages.ERROR, 'Error occured')
    return HttpResponseRedirect('/cc/')


def handler404(request, exception):
    template_name = 'error/404.html'
    if request.path.startswith('/events/'):
        template_name = 'error/event404.html'
    elif request.path.startswith('/experts/'):
        template_name = 'error/expert404.html'
    elif request.path.startswith('/companies/'):
        template_name = 'error/company404.html'
    return page_not_found(request, exception, template_name=template_name)


def ac_search_lang(request):
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


class ImportCompany(APIView):
    def get(self, request, ):
        if request.user.is_superuser:
            return render(request, "pages/importexport/import_company.html")
        else:
            return HttpResponseForbidden()

    def post(self, request, format=None):
        if request.user.is_superuser:
            try:
                excel_file = request.FILES['file']
            except MultiValueDictKeyError:
                return redirect('import_company')
            if str(excel_file).split('.')[-1] == "xls":
                data = xls_get(excel_file, column_limit=17)
            elif str(excel_file).split('.')[-1] == "xlsx":
                data = xlsx_get(excel_file, column_limit=17)
            else:
                return redirect('import_company')

            companies = data["Companies"]

            if len(companies) > 1:  # We have company data
                for company in companies:
                    if len(company) > 0:  # The row is not blank
                        if company[0] != "Name":  # This is not header
                            if len(company) < 17:
                                i = len(company)
                                while i < 17:
                                    company.append("")
                                    i += 1
                            c = Company.objects.filter(name=company[0])
                            if c.count() == 0:
                                if not company[3]:
                                    company[3] = None
                                print(company[0])
                                new_c = Company.objects.create(
                                    name=company[0],
                                    single_info=company[1],
                                    info=company[2],
                                    founded=company[3],
                                    website=company[7],
                                    linkedin_url=company[8],
                                    facebook_url=company[9],
                                    twitter_url=company[10],
                                    premium=company[11],
                                    startup=company[13],
                                    contact_email=company[15],
                                    contact_number=company[16],
                                )
                                markets = company[12].split(";")
                                for market in markets:
                                    old_market = Markets.objects.filter(market_name=market)
                                    if old_market.count() != 0:
                                        market = Markets.objects.get(market_name=market)
                                        new_c.markets.add(market)
                                    else:
                                        market = Markets.objects.create(
                                            market_name=market
                                        )
                                        new_c.markets.add(market)
                                c_type = company[14]
                                old_type = CompanyTypes.objects.filter(name=c_type)
                                if old_type.count() != 0:
                                    market = CompanyTypes.objects.get(name=c_type)
                                    new_c.type.add(market)
                                else:
                                    market = CompanyTypes.objects.create(
                                        name=c_type
                                    )
                                    new_c.type.add(market)
                                location = CompanyAddress.objects.create(
                                    location=company[4],
                                    country=company[5],
                                    city=company[6],
                                    is_primary=True,
                                )
                                new_c.location.add(location)

            experts = data["Experts"]
            if len(experts) > 1:
                for expert in experts:
                    if len(expert) > 0:
                        if expert[0] != "Name":
                            print(len(expert))
                            if len(expert) < 17:
                                i = len(expert)
                                while i < 17:
                                    expert.append("")
                                    i += 1
                            e = Expert.objects.filter(name=expert[0])
                            if e.count() == 0:
                                new_expert = Expert.objects.create(
                                    name=expert[0],
                                    business_title=expert[1],
                                    location=expert[2],
                                    country=expert[3],
                                    city=expert[4],
                                    bio=expert[5],
                                    linkedin_url=expert[7],
                                    facebook_url=expert[8],
                                    twitter_url=expert[9],
                                    personal_url=expert[10],
                                    contact=expert[11],
                                    age=expert[12],
                                )
                                skills = expert[13].split(";")
                                for skill in skills:
                                    old_skill = ExpertTags1.objects.filter(expertise_fields=skill)
                                    if old_skill.count() != 0:
                                        skill = ExpertTags1.objects.get(expertise_fields=skill)
                                        new_expert.fields_of_experties.add(skill)
                                    else:
                                        skill = ExpertTags1.objects.create(
                                            expertise_fields=skill
                                        )
                                        new_expert.fields_of_experties.add(skill)
                                industries = expert[6].split(";")
                                for ind in industries:
                                    old_ind = Industries.objects.filter(name=ind)
                                    if old_ind.count() != 0:
                                        ind = Industries.objects.get(name=ind)
                                        new_expert.industry.add(ind)
                                    else:
                                        ind = Industries.objects.create(
                                            name=ind
                                        )
                                        new_expert.industry.add(ind)
                                languages = expert[14].split(";")
                                for lang in languages:
                                    old_lang = Languages.objects.filter(language=lang)
                                    if old_lang.count() != 0:
                                        lang = Languages.objects.get(language=lang)
                                        new_expert.language.add(lang)
                                    else:
                                        lang = Languages.objects.create(
                                            language=lang
                                        )
                                        new_expert.language.add(lang)
                                company = expert[15]
                                comp = Company.objects.filter(name=company)
                                if comp.count() != 0:
                                    comp = Company.objects.get(name=company)
                                    new_expert.company.add(comp)
                                avail = expert[16]
                                if avail:
                                    avail = Availability.objects.get(type=avail)
                                    new_expert.availability.add(avail)

            return redirect('import_company')
        else:
            return HttpResponseForbidden()


def terms(request):
    if request.method == "GET":
        return render(request, "pages/other/terms.html")


def privacy(request):
    if request.method == "GET":
        return render(request, "pages/other/privacy.html")


def faq(request):
    if request.method == "GET":
        return render(request, "pages/other/faq.html")


def about(request):
    if request.method == "GET":
        return render(request, "pages/other/about.html")
