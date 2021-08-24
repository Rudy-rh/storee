from rest_framework import serializers
from utils.generals import get_model

Banner = get_model('barber', 'Banner')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
