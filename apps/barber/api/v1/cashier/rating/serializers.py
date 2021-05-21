from rest_framework import serializers
from utils.generals import get_model

OrderRating = get_model('barber', 'OrderRating')



class OrderRatingSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(read_only=True)

    class Meta:
        model = OrderRating
        fields = ('rmanagement', 'rhygiene', 'rbarberman', 'rcashier',
                  'rsuggestion', 'customer', 'create_at',)
