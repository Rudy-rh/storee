from rest_framework import serializers
from utils.generals import get_model

Information = get_model('barber', 'Information')


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'
