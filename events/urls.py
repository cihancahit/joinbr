from django.urls import path

from .views import *

urlpatterns = [
    path('', AllEventsView.as_view(), name="AllEvents"),
    # path('createevent', SubmitEventView.as_view(), name="submit_event"),
    path('search', event_search, name="submit_event"),
    path('search/<str:category>', event_search_ind, name="event_search_ind"),
    path('api/events/<slug:slug>/follow', EventFollowAPIToggle.as_view(), name="event_follow"),
    path('<slug:slug>', EventDetailView.as_view(), name='event_detail_url'),
    path('ac/search/event/name', ac_search_event, name="ac_event"),
    path('ac/search/tag', ac_search_tag, name="ac_tag"),
    path('announcement/<slug:slug>', AggEventDetailView.as_view(), name='aggevent_detail_url'),
    path('searchevent/', searchEvent, name='searchevent'),
    path('buyticket/<int:pk>/', buy_ticket, name='buy_ticket'),
    path('buyticket/soon/', temp_purchasing, name='temp_purchasing'),  # TEMP. PATH FOR PURCHASING
    path('buyticket/purchased', purchased_ticket, name='purchased_ticket'),
    path('postevent/', post_event, name="post_event"),
    path('c/<slug:slug>', category_detail, name="category_detail"),
    path('country/<str:country>', event_search_country, name="event_search_country"),
    path('date/<str:date>', event_search_comp, name="event_search_comp"),
    path('date/<str:date>/<str:country>/<str:city>', event_search_c_c_i, name="event_search_c_c_i"),
    path('country/<str:country>/<str:city>', event_search_city, name="event_search_city"),
    path('<str:category>/date/<str:date>/<str:country>', event_search_i_c_c, name="event_search_i_c_c"),
    path('<str:category>/<str:date>/<str:country>/<str:city>', event_search_4, name="event_search4"),
    path('category/<str:category>/<str:country>', event_search_ind_country, name="event_search_ind_country"),
    path('date/<str:date>/<str:country>', event_search_comp_country, name="event_search_ind_country"),
    path('<str:category>/<str:country>/<str:city>', event_search_3, name="event_search3"),
    path('<str:category>/<str:date>', event_search_ind_comp, name="event_search_ind_comp"),
    path('filtereventd/', filter_event_date, name='filtereventd'),
    path('filtereventc/', filter_event_cat, name='filtereventc'),
    path('filtereventp/', filter_event_price, name='filtereventp'),
    path('api/events/search', EventSearchAPi.as_view(), name="event_search_api"),
    path('ebcallback', EventSearchAPi.as_view(), name="event_search_api"),
    path('add_sub/<slug:slug>', add_organizer_subscriber, name="add_organizer_subscriber"),
]
