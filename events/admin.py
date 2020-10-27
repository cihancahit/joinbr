from django.contrib import admin

from .models import *
from .forms import AggrEventsForm


class EventAdmin(admin.ModelAdmin):
    list_display = ('get_image_thumbnail_admin', 'name', 'info')
    filter_horizontal = ['category', 'sponsor', 'follower_list', 'tag', 'organizer']
    search_fields = ["name", "info"]


class AggrEventsAdmin(admin.ModelAdmin):
    form = AggrEventsForm
    list_display = ('name', 'location', 'source')
    filter_horizontal = ['company']
    search_fields = ["name"]


class EventSponsorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


admin.site.register(AggrEvents, AggrEventsAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(EventSponsors)
admin.site.register(Tags)
