from rest_framework import serializers
from utils.generals import get_model

Rules = get_model('barber', 'Rules')


class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rules
        fields = '__all__'
