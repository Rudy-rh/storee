from rest_framework import serializers
from utils.generals import get_model

Branch = get_model('barber', 'Branch')


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('uuid', 'name', 'address', 'latitude', 'longitude', 'icon',)
