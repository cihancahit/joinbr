from rest_framework import serializers

from .models import ReviewModel


class PostedReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewModel
        fields = '__all__'
        depth = 2

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['username'] = data['user'].pop('user')
        data['username'] = data['username']['fullname']
        return data
