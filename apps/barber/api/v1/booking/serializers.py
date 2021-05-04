from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from utils.generals import get_model

UserModel = get_user_model()
Booking = get_model('barber', 'Booking')
StyleItem = get_model('barber', 'StyleItem')
BranchBarberman = get_model('barber', 'BranchBarberman')


class CreateBookingSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
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
    url = serializers.HyperlinkedIdentityField(view_name='barber_api:booking-detail',
                                               lookup_field='uuid', read_only=True)
    reserved_type = serializers.SerializerMethodField()
    styleitem = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_reserved_type(self, instance):
        return instance.get_reserved_type_display()

    def get_styleitem(self, instance):
        if instance.styleitem is None:
            return None
        return instance.styleitem.label

    def get_date(self, instance):
        return timezone.datetime.combine(instance.reserved_date, instance.reserved_time)

    def get_status(self, instance):
        return instance.get_status_display()


class ListBookingSerializer(BaseBookingSerializer):
    class Meta:
        model = Booking
        fields = ('create_at', 'date', 'reserved_date', 'reserved_time', 'url',
                  'uuid', 'reserved_type', 'styleitem', 'status', 'note',)


class RetrieveBookingSerializer(BaseBookingSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
