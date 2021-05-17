from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from utils.generals import get_model

UserModel = get_user_model()
Booking = get_model('barber', 'Booking')
BookingRating = get_model('barber', 'BookingRating')
StyleItem = get_model('barber', 'StyleItem')
BranchBarberman = get_model('barber', 'BranchBarberman')


class BaseBookingRatingSerializer(serializers.ModelSerializer):
    booking = serializers.UUIDField(source='booking.uuid', read_only=True)
    rating_avg = serializers.SerializerMethodField()

    def get_rating_avg(self, instance):
        rmanagement = getattr(instance, 'rmanagement', 0)
        rhygiene = getattr(instance, 'rhygiene', 0)
        rbarberman = getattr(instance, 'rbarberman', 0)
        rcashier = getattr(instance, 'rcashier', 0)

        x = (rmanagement + rhygiene + rbarberman + rcashier) / 4
        return x


class CreateBookingRatingSerializer(BaseBookingRatingSerializer):
    class Meta:
        model = BookingRating
        fields = ('rmanagement', 'rhygiene', 'rbarberman', 'rcashier',
                  'rsuggestion', )

    def validate(self, data):
        booking = self.context.get('booking', None)
        if booking.status != Booking.Status.DONE:
            raise serializers.ValidationError(detail=_("Belum boleh memberi rating sampai selesai dilayani"))
        return super().validate(data)
    
    @transaction.atomic()
    def create(self, validated_data):
        booking = self.context.get('booking', None)
        defaults = {
            'rmanagement': validated_data.pop('rmanagement'),
            'rhygiene': validated_data.pop('rhygiene'),
            'rbarberman': validated_data.pop('rbarberman'),
            'rcashier': validated_data.pop('rcashier'),
            'rsuggestion': validated_data.pop('rsuggestion')
        }
        instance, _created = BookingRating.objects \
            .update_or_create(booking=booking, defaults=defaults, **validated_data)
        return instance


class RetrieveBookingRatingSerializer(BaseBookingRatingSerializer):
    class Meta:
        model = BookingRating
        fields = '__all__'



class CreateBookingSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    barberman = serializers.SlugRelatedField(slug_field='uuid', write_only=False,
                                             queryset=BranchBarberman.objects.all())
    styleitem = serializers.SlugRelatedField(slug_field='uuid', write_only=False,
                                             queryset=StyleItem.objects.all(),
                                             required=False)

    class Meta:
        model = Booking
        fields = ('customer', 'barberman', 'reserved_type',
                  'reserved_date', 'reserved_time', 'styleitem',
                  'note',)
        extra_kwargs = {
            'barberman': {'required': True},
            'styleitem': {
                'allow_blank': True,
                'allow_null': True,
                'required': False
            }
        }


class BaseBookingSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='barber_api:customer:booking-detail',
                                               lookup_field='uuid', read_only=True)
    reserved_type = serializers.SerializerMethodField()
    styleitem = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    rating = RetrieveBookingRatingSerializer(read_only=True)

    def get_reserved_type(self, instance):
        return instance.get_reserved_type_display()

    def get_styleitem(self, instance):
        if instance.styleitem is None:
            return None
        return instance.styleitem.label

    def get_date(self, instance):
        return timezone.datetime.combine(instance.reserved_date, instance.reserved_time)

    def get_status_display(self, instance):
        return instance.get_status_display()


class ListBookingSerializer(BaseBookingSerializer):
    class Meta:
        model = Booking
        fields = ('create_at', 'date', 'reserved_date', 'reserved_time', 'url',
                  'uuid', 'reserved_type', 'styleitem', 'status', 'status_display', 
                  'note', 'rating',)


class RetrieveBookingSerializer(BaseBookingSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
