from django.contrib.auth.models import Group

from rest_framework import serializers
from utils.generals import get_model

WorkStandardCategory = get_model('barber', 'WorkStandardCategory')


class GroupSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='barber_api:general:group-detail',
                                               lookup_field='id', read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'url',)


class WorkStandardCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkStandardCategory
        fields = ('uuid', 'label', 'standard_sections',)
        depth = 1
