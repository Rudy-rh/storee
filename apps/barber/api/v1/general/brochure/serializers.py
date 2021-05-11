from rest_framework import serializers
from utils.generals import get_model

Brochure = get_model('barber', 'Brochure')


class BrochureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brochure
        fields = '__all__'
