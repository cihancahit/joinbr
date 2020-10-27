from django.contrib import admin

from .models import Organizer, OrganizerEventsPhotos, OrganizerSubscribers

admin.site.register(Organizer)
admin.site.register(OrganizerEventsPhotos)
admin.site.register(OrganizerSubscribers)
