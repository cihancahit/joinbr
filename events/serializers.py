from rest_framework import serializers

from events.models import Event
from users.models import UserProfileModel


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user
        event = Event.objects.get(slug=data['slug'])
        if user.is_authenticated:
            user_profile = UserProfileModel.objects.get(user=user)
            if user_profile in event.follower_list.all():
                following = True
            else:
                following = False
            data['follower_list'] = following
        else:
            data['follower_list'] = False
        return data
