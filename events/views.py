import json
import json as json2
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, ListView
from hitcount.views import HitCountDetailView
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from custom.custom_tools2 import get_user
from events.serializers import EventSerializer
from expert.models import Expert, ExpertEvents
from fec_app.views import BaseContext
from organizer.models import Organizer, OrganizerEventsPhotos, OrganizerSubscribers
from .forms import EventForm, BuyTicketForm
from .models import *


class AllEventsView(BaseContext, ListView):
    template_name = "pages/events/all_events2.html"
    context_object_name = "events"

    sort_type = 'alphabetic-asc'
    paginate_by = 10
    filter_type = '*'
    event_list1 = {}

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        if self.request.GET.get('paginate_by'):
            self.request.session['pageev'] = self.request.GET.get('paginate_by')
        else:
            self.request.session['pageev'] = self.paginate_by
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        if self.request.GET.get('sort'):
            self.sort_type = self.request.GET.get('sort')
        if self.request.GET.get('filter'):
            self.filter_type = self.request.GET.get('filter')

        if self.filter_type == '*':
            event_list = Event.objects.all()
        elif self.filter_type == 'for_you':
            if self.request.user.is_authenticated:
                profile = UserProfileModel.objects.get(user=self.request.user)
                # Get category list from user's following events.
                cat_list = []
                event_list = []
                for event in profile.followed_events.all():
                    event_list.append(event.pk)
                    for cat in event.category.all():
                        cat_list.append(cat)
                event_list = Event.objects.filter(category__in=cat_list).exclude(pk__in=event_list)
        elif self.filter_type == 'free':
            event_list = Event.objects.filter(ticket_type="free")
        elif self.filter_type == 'this_week':
            now = datetime.now()
            start = now - timedelta(days=now.weekday())
            end = start + timedelta(days=6)
            q_event_date_st = start.strftime("%Y-%m-%d")
            q_event_date_end = end.strftime("%Y-%m-%d")
            event_list = Event.objects.filter(
                Q(
                    start_event_dt__gte=q_event_date_st),
                Q(
                    start_event_dt__lte=q_event_date_end)
            )
        elif self.filter_type == 'next_week':
            print('nw')
            now = datetime.now()
            start = now - timedelta(days=now.weekday())
            start = start + timedelta(days=6)
            end = start + timedelta(days=13)
            q_event_date_st = start.strftime("%Y-%m-%d")
            q_event_date_end = end.strftime("%Y-%m-%d")
            event_list = Event.objects.filter(
                Q(
                    start_event_dt__gte=q_event_date_st),
                Q(
                    start_event_dt__lte=q_event_date_end)
            )
        else:
            event_list = Event.objects.all()

        if self.sort_type == 'relevancy':
            # TODO relevancy will be added
            event_list = event_list.order_by("-id")
        elif self.sort_type == 'alphabetic-asc':
            event_list = event_list.order_by("name")
        elif self.sort_type == 'alphabetic-desc':
            event_list = event_list.order_by("-name")
        elif self.sort_type == 'popularity':
            # TODO popularity will be added
            event_list = event_list.order_by("id")
        else:
            event_list = event_list.order_by("-id")

        self.event_list1 = event_list
        return event_list

    def get_context_data(self, **kwargs):
        context = super(AllEventsView, self).get_context_data(**kwargs)
        context["aggr_events"] = AggrEvents.objects.filter(is_approved=True)
        context["categories"] = Category.objects.all()[:16]
        context["event_active"] = "menu-active"
        context["logged_user"] = get_user(self.request)
        if self.request.session.get('pageev'):
            context["pageev"] = self.request.session.get('pageev')
        context["sort_type"] = self.request.session['sort_type'] = self.sort_type
        context["filter_type"] = self.request.session['filter_type'] = self.filter_type
        context["event_count"] = self.event_list1.count()
        return context


class SubmitEventView(LoginRequiredMixin, FormView):
    template_name = 'pages/events/create_event.html'
    form_class = EventForm
    success_url = reverse_lazy('index_url')

    def form_valid(self, form):
        event = form.save()

        Ticket.objects.create(
            event=event,
            name=event.name,
            quota_left=event.quantity,
            description="",
            active=True,
            price=event.price,
            ticket_type=event.ticket_type
        )

        return super().form_valid(form)


class EventDetailView(BaseContext, HitCountDetailView):
    model = Event
    template_name = 'pages/events/event_detail2.html'
    context_object_name = 'event'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        context["event_active"] = "menu-active"
        context["logged_user"] = get_user(self.request)
        context["speakers"] = ExpertEvents.objects.filter(event__slug=self.kwargs['slug'])
        context["reviews"] = ReviewModel.objects.filter(event__slug=self.kwargs['slug'])
        organizer = Event.objects.get(slug=self.kwargs['slug']).organizer.all()
        context["events_photos_row1"] = OrganizerEventsPhotos.objects.filter(organizer__in=organizer)[:4]
        context["events_photos_row2"] = OrganizerEventsPhotos.objects.filter(organizer__in=organizer)[4:8]
        context["events_live"] = Event.objects.filter(organizer__in=organizer,
                                                      start_event_dt__gte=datetime.today())
        context["events_past"] = Event.objects.filter(organizer__in=organizer,
                                                      start_event_dt__lt=datetime.today())
        cat = Event.objects.get(slug=self.kwargs['slug']).category.all()
        context["similar_event"] = Event.objects.filter(category__in=cat)[:1]

        return context


def add_organizer_subscriber(request, slug):
    if request.method == 'POST':
        email = request.POST.get('sub-email')
        OrganizerSubscribers.objects.create(
            organizer=Event.objects.get(slug=slug).organizer,
            email=email
        )
        messages.add_message(request, messages.SUCCESS, 'Thank you for your inquiry')
        return redirect("event_detail_url", slug=slug)
    else:
        return HttpResponse("Error")



class AggEventDetailView(BaseContext, DetailView):
    model = AggrEvents
    template_name = 'pages/events/agg_event_detail.html'
    context_object_name = 'aggevent'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        context["event_active"] = "menu-active"
        context["logged_user"] = get_user(self.request)
        return context


def searchEvent(request):
    if request.is_ajax():
        q_event_name = request.POST.get('event_name')
        q_event_loc = request.POST.get('event_loc')
        q_event_date = request.POST.get('event_date')
        # return JsonResponse(dict(events=list(Event.objects.values('name', 'info'))))

        return JsonResponse(
            serializers.serialize('json', Event.objects.filter(
                Q(name__icontains=q_event_name) & Q(location__icontains=q_event_loc) & Q(
                    start_event_dt__icontains=q_event_date))),
            safe=False)


def buy_ticket(request, pk):
    event = Event.objects.get(pk=pk)
    ticket = Ticket.objects.get(event=event)
    form = BuyTicketForm(instance=ticket)

    context = {
        'event': event,
        'form': form,
        'ticket': ticket,
    }

    if request.method == 'POST':
        form = BuyTicketForm(request.POST)
        if form.is_valid():
            requested_ticket_count = form.cleaned_data.get('quantiy')
            ticket.quota_left = ticket.quota_left - requested_ticket_count
            ticket.save()

            request.session['purchased_ticket'] = ticket.id
            request.session['requested_ticket_count'] = str(requested_ticket_count)
            request.session['total_price'] = str(ticket.price * requested_ticket_count)
            request.session['bro_pints'] = str((ticket.price * requested_ticket_count) * 10 / 100)
            request.session['event_category'] = event.category.pk

            # If ticket type is donation:
            if ticket.ticket_type == "Donation":
                request.session['total_price'] = str(
                    form.cleaned_data.get('donation_price') * requested_ticket_count
                )
                request.session['bro_pints'] = str(
                    (form.cleaned_data.get('donation_price') * requested_ticket_count) * 10 / 100
                )

            return redirect('purchased_ticket')

    return render(request, 'pages/events/buy_ticket.html', context)


def temp_purchasing(request):
    return render(request, 'pages/events/dummy_ticket.html', )


def purchased_ticket(request):
    ticket_id = request.session.get('purchased_ticket')
    event_category = request.session.get('event_category')
    related_events = Event.objects.filter(category=event_category).order_by("-finish_event_dt")[:4]
    # related_events = related_events.objects.filter(category=event_category)
    context = {
        'ticket': Ticket.objects.get(pk=ticket_id),
        'requested_ticket_count': request.session.get('requested_ticket_count'),
        'total_price': request.session.get('total_price'),
        'bro_pints': request.session.get('bro_pints'),
        'related_events': related_events,
    }
    return render(request, 'pages/events/purchased_ticket.html', context)


def post_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        organizer = request.POST.get('organizer')
        location = request.POST.get('location')
        start_dt = request.POST.get('start_dt')
        end_dt = request.POST.get('end_dt')
        price = request.POST.get('price')
        lang = request.POST.get('lang')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        ticket_type = request.POST.get('ticket_type')
        category = Category.objects.get(name=request.POST.get('category'))
        speaker = Expert.objects.get(name=request.POST.get('speaker'))
        event_img = request.FILES.get('file')

        event = Event.objects.create(
            name=name,
            category=category,
            location=location,
            organizer=organizer,
            speaker=speaker,
            start_event_dt=start_dt,
            finish_event_dt=end_dt,
            ticket_type=ticket_type,
            price=price,
            quantity=quantity,
            language=lang,
            info=description,
            event_img=event_img
        )

        Ticket.objects.create(
            event=event,
            name=event.name,
            quota_left=event.quantity,
            description="",
            active=True,
            price=event.price,
            ticket_type=ticket_type
        )

        response_data = {'result': 'Create post successful!', 'ad': "banan"}

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    related_events = Event.objects.filter(category=category).order_by("-start_event_dt")
    # free_events = Event.objects.filter(category=category, price='Free').order_by("-start_event_dt")
    all_category = Category.objects.all()
    experts = Expert.objects.all()[:4]

    context = {
        'category': category,
        'related_events': related_events,
        'free_events': related_events,
        'all_category': all_category,
        'logged_user': get_user(request),
        'experts': experts,
        'event_active': 'menu-active'
    }
    return render(request, 'pages/events/category_detail.html', context)


def event_search_country(request, country, ):
    if request.POST:
        context = {}
        name = request.POST.get('event_name')
        country = country
        country = country.replace("-", " ")
        events = Event.objects.filter(
            # Q(name__icontains=name) &
            Q(location__icontains=country)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["country"] = country
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of events in <span class="event-title-cat-span">' \
                                + country + '</span>'
        context["event_active"] = "menu-active"
        context["logged_user"] = get_user(request)

        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        context[
            "page_title"] = 'l<span style="color: #08c65b;">Reveal</span> ist of events in <span class="event-title-cat-span">' \
                            + country + '</span>'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", )


def event_search_city(request, country, city):
    if request.POST:
        context = {}
        name = request.POST.get('event_name')
        country = country
        city = city
        country = country.replace("-", " ")
        city = city.replace("-", " ")
        events = Event.objects.filter(
            # Q(name__icontains=name) &
            Q(location__icontains=country) &
            Q(city__icontains=city)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["country"] = country
        context["city"] = city
        context["logged_user"] = get_user(request)
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of events in <span class="event-title-cat-span">' \
                                + city + ', ' + country + '</span>'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        context[
            "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of events in <span class="event-title-cat-span">' \
                            + city + ', ' + country + '</span>'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", )


def event_search_3(request, category, country, city):
    if request.POST:
        context = {}
        name = request.POST.get('event_name')
        category = category
        country = country
        city = city
        country = country.replace("-", " ")
        category = category.replace("-", " ")
        city = city.replace("-", " ")
        events = Event.objects.filter(
            # Q(name__icontains=name) &
            Q(category__name__icontains=category) &
            Q(location__icontains=country) &
            Q(city__icontains=city)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["category"] = category
        context["country"] = country
        context["city"] = city
        context["logged_user"] = get_user(request)
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events in <span class="event-title-cat-span">' + country + ', ' + city + '</span>'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        context[
            "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events in <span class="event-title-cat-span">' + country + ', ' + city + '</span>'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", )


def event_search_c_c_i(request, date, country, city):
    if request.POST:
        context = {}
        name = request.POST.get('event_name')
        date = date
        country = country
        city = city
        country = country.replace("-", " ")
        city = city.replace("-", " ")
        events = Event.objects.filter(
            # Q(name__icontains=name) &
            Q(start_event_dt__icontains=date) &
            Q(location__icontains=country) &
            Q(city__icontains=city)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["date"] = date
        context["country"] = country
        context["city"] = city
        context["logged_user"] = get_user(request)

        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + city + ', ' + country + '</span> events  in ' + date
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        context[
            "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + city + ', ' + country + '</span> events  in ' + date
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", )


def event_search_4(request, category, date, country, city):
    if request.POST:
        context = {}
        name = request.POST.get('event_name')
        category = category
        date = date
        country = country
        city = city
        country = country.replace("-", " ")
        category = category.replace("-", " ")
        city = city.replace("-", " ")
        events = Event.objects.filter(
            # Q(name__icontains=name) &
            Q(category__name__icontains=category) &
            Q(start_event_dt__icontains=date) &
            Q(location__icontains=country) &
            Q(city__icontains=city)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["category"] = category
        context["date"] = date
        context["country"] = country
        context["city"] = city
        context["logged_user"] = get_user(request)
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events in <span class="event-title-cat-span">' + country + ', ' + city + '</span> for ' + date
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        context[
            "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events in <span class="event-title-cat-span">' + country + ', ' + city + '</span> for ' + date
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", )


def event_search_i_c_c(request, category, date, country, ):
    if request.POST:
        context = {}
        name = request.POST.get('event_name')
        category = category
        date = date
        country = country
        country = country.replace("-", " ")
        category = category.replace("-", " ")
        events = Event.objects.filter(
            # Q(name__icontains=name) &
            Q(category__name__icontains=category) &
            Q(start_event_dt__icontains=date) &
            Q(location__icontains=country)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["category"] = category
        context["date"] = date
        context["country"] = country
        context["logged_user"] = get_user(request)
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events in <span class="event-title-cat-span">' + country + '</span> for ' + date
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        context[
            "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events in <span class="event-title-cat-span">' + country + '</span> for ' + date
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", )


def event_search_ind_country(request, category, country, ):
    if request.POST:
        context = {}
        name = request.POST.get('event_name')
        category = category
        country = country
        country = country.replace("-", " ")
        category = category.replace("-", " ")
        events = Event.objects.filter(
            # Q(name__icontains=name) &
            Q(category__name__icontains=category) &
            Q(location__icontains=country)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["category"] = category
        context["country"] = country
        context["logged_user"] = get_user(request)
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events in <span class="event-title-cat-span">' + country + '</span>'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        context[
            "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events in <span class="event-title-cat-span">' + country + '</span>'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", )


def event_search_comp_country(request, date, country, ):
    if request.POST:
        context = {}
        name = request.POST.get('event_name')
        date = date
        country = country
        country = country.replace("-", " ")
        events = Event.objects.filter(
            # Q(name__icontains=name) &
            Q(start_event_dt__icontains=date) &
            Q(location__icontains=country)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["date"] = date
        context["country"] = country
        context["logged_user"] = get_user(request)
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + country + '</span> events  in ' + date
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        context[
            "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + country + '</span> events  in ' + date
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", )


def event_search_ind_comp(request, category, date, ):
    if request.POST:
        context = {}
        name = request.POST.get('event_name')
        date = date
        category = category
        category = category.replace("-", " ")
        events = Event.objects.filter(
            # Q(name__icontains=name) &
            Q(start_event_dt__icontains=date) &
            Q(category__name__icontains=category)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["date"] = date
        context["category"] = category
        context["logged_user"] = get_user(request)
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events in <span class="event-title-cat-span">' + date + '</span>'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", context)
        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        context[
            "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events in <span class="event-title-cat-span">' + date + '</span>'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", )


def event_search_ind(request, category, ):
    if request.POST:
        context = {}
        name = request.POST.get('event_name')
        category = category
        category = category.replace("-", " ")
        events = Event.objects.filter(
            # Q(name__icontains=name) &
            Q(category__name__icontains=category)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["category"] = category
        context["logged_user"] = get_user(request)
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events from all over the World'

        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        category = category
        category = category.replace("-", " ")
        events = Event.objects.filter(
            Q(category__name__icontains=category)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of <span class="event-title-cat-span">' + category + '</span> events from all over the World'
        context["category"] = category
        context["logged_user"] = get_user(request)
        return render(request, "pages/events/all_events_search2.html", context)


def event_search(request, ):
    if request.POST:
        context = {}
        name = request.POST.get('main-search')
        events = Event.objects.filter(
            Q(name__icontains=name)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["logged_user"] = get_user(request)
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of events from all over the world'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        context["page_title"] = '<span style="color: #08c65b;">Reveal</span> list of events from all over the world'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", )


def event_search_comp(request, date, ):
    if request.POST:
        context = {}
        name = request.POST.get('event_name')
        date = date
        events = Event.objects.filter(
            Q(start_event_dt__icontains=date)
        ).order_by("-id")
        context["events"] = events
        context["categories"] = Category.objects.all()
        context["name"] = name
        context["date"] = date
        if events.count() == 0:
            context[
                "page_title"] = 'Oups, that is strange! We haven\'t found any event for your search request. Why don\'t you check other options. We have many...'
        else:
            context[
                "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of events  in <span class="event-title-cat-span">' \
                                + date + '</span> from all over the world'
        context["event_active"] = "menu-active"
        context["logged_user"] = get_user(request)
        return render(request, "pages/events/all_events_search2.html", context)
    else:
        context = {}
        context[
            "page_title"] = '<span style="color: #08c65b;">Reveal</span> list of events  in <span class="event-title-cat-span">' \
                            + date + '</span> from all over the world'
        context["event_active"] = "menu-active"
        return render(request, "pages/events/all_events_search2.html", )


def filter_event_date(request):
    if request.is_ajax():
        q_event_date = request.POST.get('event_date')

        if q_event_date == 'Today':
            now = datetime.now()
            q_event_date1 = now.strftime("%Y-%m-%d")
            response = JsonResponse(
                serializers.serialize('json', Event.objects.filter(Q(start_event_dt__icontains=q_event_date1))),
                safe=False)
        elif q_event_date == 'Tomorrow':
            tomorrow = datetime.today() + timedelta(days=1)
            q_event_date1 = tomorrow.strftime("%Y-%m-%d")
            response = JsonResponse(
                serializers.serialize('json', Event.objects.filter(Q(start_event_dt__icontains=q_event_date1))),
                safe=False)
        elif q_event_date == 'This Week':
            now = datetime.now()
            start = now - timedelta(days=now.weekday())
            end = start + timedelta(days=6)
            q_event_date_st = start.strftime("%Y-%m-%d")
            q_event_date_end = end.strftime("%Y-%m-%d")
            response = JsonResponse(
                serializers.serialize('json', Event.objects.filter(Q(
                    start_event_dt__gte=q_event_date_st), Q(
                    start_event_dt__lte=q_event_date_end))),
                safe=False)
        elif q_event_date == 'Next Week':
            now = datetime.now()
            start = now - timedelta(days=now.weekday())
            start = start + timedelta(days=6)
            end = start + timedelta(days=13)
            q_event_date_st = start.strftime("%Y-%m-%d")
            q_event_date_end = end.strftime("%Y-%m-%d")
            response = JsonResponse(
                serializers.serialize('json', Event.objects.filter(Q(
                    start_event_dt__gte=q_event_date_st), Q(
                    start_event_dt__lte=q_event_date_end))),
                safe=False)

    return response


def filter_event_cat(request):
    if request.is_ajax():
        q_event_cat = request.POST.get('event_cat')
        cat = Category.objects.get(id=q_event_cat)
        return JsonResponse(
            serializers.serialize('json', Event.objects.filter(Q(category=cat))),
            safe=False)


def filter_event_price(request):
    if request.is_ajax():
        q_event_price = request.POST.get('event_price')
        return JsonResponse(
            serializers.serialize('json', Event.objects.filter(ticket_type=q_event_price)),
            safe=False)


class EventFollowAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = Event.objects.get(slug=slug)
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


class EventSearchAPi(APIView):
    # TODO errors will be improved(eventbrite api)
    parser_classes = [JSONParser]

    def post(self, request, **kwargs, ):

        if "dates" in request.data:
            q_date = request.data["dates"]
            if q_date == "this_week":
                now = datetime.now()
                start = now - timedelta(days=now.weekday())
                end = start + timedelta(days=6)
                q_event_date_st = start.strftime("%Y-%m-%d")
                q_event_date_end = end.strftime("%Y-%m-%d")
                queryset = Event.objects.filter(
                    Q(
                        start_event_dt__gte=q_event_date_st),
                    Q(
                        start_event_dt__lte=q_event_date_end)
                )[:12]
                # need development static to dynamic author: SI
                serializer = EventSerializer(queryset, many=True, context={"request": request})
                response = serializer.data
            elif q_date == "next_week":
                now = datetime.now()
                start = now - timedelta(days=now.weekday())
                start = start + timedelta(days=6)
                end = start + timedelta(days=13)
                q_event_date_st = start.strftime("%Y-%m-%d")
                q_event_date_end = end.strftime("%Y-%m-%d")
                queryset = Event.objects.filter(
                    Q(
                        start_event_dt__gte=q_event_date_st),
                    Q(
                        start_event_dt__lte=q_event_date_end)
                )[:12]
                # need development static to dynamic author: SI
                serializer = EventSerializer(queryset, many=True, context={"request": request})
                response = serializer.data
            else:
                response = "ARGUMENTS_ERROR: Invalid date"
            return Response(response)
        elif "price" in request.data:
            q_price = request.data["price"]
            if q_price == "free":
                queryset = Event.objects.filter(
                    ticket_type="free"
                )[:12]
                # need development static to dynamic author: SI
                serializer = EventSerializer(queryset, many=True, context={"request": request})
                response = serializer.data
            else:
                response = "ARGUMENTS_ERROR: Invalid price"
            return Response(response)
        elif "special" in request.data:
            if self.request.user.is_authenticated:
                profile = UserProfileModel.objects.get(user=self.request.user)
                # Get category list from user's following events.
                cat_list = []
                event_list = []
                for event in profile.followed_events.all():
                    event_list.append(event.pk)
                    for cat in event.category.all():
                        cat_list.append(cat)
                queryset = Event.objects.filter(category__in=cat_list).exclude(pk__in=event_list)[:12]
                # need development static to dynamic author: SI
                serializer = EventSerializer(queryset, many=True, context={"request": request})
                response = serializer.data
                return Response(response)
            else:
                return Response(status.HTTP_401_UNAUTHORIZED)
        elif "all" in request.data:
            q_all = request.data["all"]
            if q_all == "*":
                queryset = Event.objects.all().order_by("-id")[:12]
                # need development static to dynamic author: SI
                serializer = EventSerializer(queryset, many=True, context={"request": request})
                response = serializer.data
            else:
                response = "ARGUMENTS_ERROR: Invalid price"
            return Response(response)
        else:
            response = "No target in given data"
        return Response(response)


def eb_get(request):
    if request.GET:
        if Expert.objects.filter(slug=request.GET['state']).exists():
            code = request.GET['code']
            slug = request.GET['state']
            url = 'https://www.eventbrite.com/oauth/token'
            params = {
                'client_id': settings.EB_CLIENT_ID,
                'grant_type': 'authorization_code',
                'redirect_uri': settings.EB_REDIRECT_URI,
                'code': code,
                'client_secret': settings.EB_CLIENT_SECRET,
            }
            response = requests.post(url, params=params)
            if response.status_code == 200:
                response = response.json()
                auth_token = response['access_token']
                print(auth_token)


# expert profile search event
def ac_search_event(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Event.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            event = {}
            event["id"] = r.pk
            event["name"] = r.name
            event["slug"] = r.slug
            event["sdate"] = r.start_event_dt.strftime("%M %d,%y")
            event["img"] = r.event_img.url
            results.append(event)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# expert profile create event tag search
def ac_search_tag(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Tags.objects.filter(tag_name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.tag_name)
        data = json2.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
