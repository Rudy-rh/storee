from django.db import transaction
from rest_framework import serializers
from utils.generals import get_model

Information = get_model('barber', 'Information')
InformationRead = get_model('barber', 'InformationRead')


class InformationSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='barber_api:general:information-detail',
                                               lookup_field='uuid', read_only=True)

    class Meta:
        model = Information
        fields = '__all__'


class MarkReadInformationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    information = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Information.objects.all()
    )

    class Meta:
        model = InformationRead
        fields = ('user', 'information',)

    @transaction.atomic
    def create(self, validate_data):
        instance, _created = self.Meta.model.objects \
            .get_or_create(**validate_data)

        return instance
