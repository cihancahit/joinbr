from django.template.defaultfilters import safe
from django.utils.html import strip_tags,html_safe
from django.utils.safestring import SafeString
from rest_framework import serializers

from events.models import Event
from expert.models import ExpertEvents


# class EventSerializer(serializers.ModelSerializer):
#     photo_url = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Event
#         fields = ('name', 'info', 'photo_url', 'ticket_type', 'slug')
#
#     def get_photo_url(self, event):
#         request = self.context.get('request')
#         photo_url = event.event_img.url
#         return request.build_absolute_uri(photo_url)
#
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['info'] = strip_tags(instance.info)
#         data['info'] = data['info'][:200]
#         data['slug'] = "/events/" + data['slug']
#         return data


class ExpertEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpertEvents
        fields = ('event', 'tag',)
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['event']['info'] = SafeString(strip_tags(instance.event.info))[:200]
        data['event']['slug'] = "/events/" + data['event']['slug']
        return data