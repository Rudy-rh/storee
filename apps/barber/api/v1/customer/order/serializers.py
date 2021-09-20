import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models.aggregates import Count
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify

from rest_framework import serializers
from utils.generals import get_model

UserModel = get_user_model()
Order = get_model('barber', 'Order')
OrderRating = get_model('barber', 'OrderRating')
OrderAssigned = get_model('barber', 'OrderAssigned')
OrderAttachment = get_model('barber', 'OrderAttachment')
StyleItem = get_model('barber', 'StyleItem')
BranchBarberman = get_model('barber', 'BranchBarberman')


def validate_attachment(file):
    name, ext = os.path.splitext(file.name)
    fsize = file.size / 1000
    if fsize > 15000:
        raise serializers.ValidationError(
            {'detail': _("Ukuran file maksimal 15 MB")})

    if ext != '.jpeg' and ext != '.jpg' and ext != '.png':
        raise serializers.ValidationError(
            {'detail': _("Jenis file tidak diperbolehkan")})


def handle_upload_attachment(instance, file):
    if instance and file:
        name, ext = os.path.splitext(file.name)
        validate_attachment(file)

        filename = slugify(name)
        instance.file.save('%s%s' % (filename, ext), file, save=False)
        instance.save(update_fields=['file'])


class OrderAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAttachment
        fields = '__all__'


class BaseOrderRatingSerializer(serializers.ModelSerializer):
    order = serializers.UUIDField(source='order.uuid', read_only=True)
    rating_avg = serializers.SerializerMethodField()

    def get_rating_avg(self, instance):
        rmanagement = getattr(instance, 'rmanagement', 0)
        rhygiene = getattr(instance, 'rhygiene', 0)
        rbarberman = getattr(instance, 'rbarberman', 0)
        rcashier = getattr(instance, 'rcashier', 0)

        x = (rmanagement + rhygiene + rbarberman + rcashier) / 4
        return x


class CreateOrderRatingSerializer(BaseOrderRatingSerializer):
    class Meta:
        model = OrderRating
        fields = ('rmanagement', 'rhygiene', 'rbarberman', 'rcashier',
                  'rsuggestion', )

    def validate(self, data):
        order = self.context.get('order', None)
        if order.status != Order.Status.DONE:
            raise serializers.ValidationError(
                detail=_("Belum boleh memberi rating sampai selesai dilayani"))
        return super().validate(data)

    @transaction.atomic()
    def create(self, validated_data):
        order = self.context.get('order', None)
        defaults = {
            'rmanagement': validated_data.pop('rmanagement'),
            'rhygiene': validated_data.pop('rhygiene'),
            'rbarberman': validated_data.pop('rbarberman'),
            'rcashier': validated_data.pop('rcashier'),
            'rsuggestion': validated_data.pop('rsuggestion')
        }
        instance, _created = OrderRating.objects \
            .get_or_create(order=order, defaults=defaults, **validated_data)
        return instance


class RetrieveOrderRatingSerializer(BaseOrderRatingSerializer):
    class Meta:
        model = OrderRating
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    barberman = serializers.SlugRelatedField(slug_field='uuid', write_only=False,
                                             queryset=BranchBarberman.objects.all())
    styleitem = serializers.SlugRelatedField(slug_field='uuid', write_only=False,
                                             queryset=StyleItem.objects.all(),
                                             required=False)

    class Meta:
        model = Order
        fields = ('customer', 'barberman', 'reserved_type',
                  'reserved_date', 'reserved_time', 'styleitem',
                  'note', 'is_booking',)
        extra_kwargs = {
            'barberman': {'required': True},
            'styleitem': {
                'allow_blank': True,
                'allow_null': True,
                'required': False
            }
        }


class CreateOrderByTakePhotoSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(slug_field='username', write_only=False,
                                            queryset=UserModel.objects.all())
    barberman = serializers.SlugRelatedField(slug_field='username', write_only=False,
                                             queryset=UserModel.objects.filter(groups__name='Barberman'))
    styleitem = serializers.SlugRelatedField(slug_field='uuid', write_only=False,
                                             queryset=StyleItem.objects.all(),
                                             required=False)

    class Meta:
        model = Order
        fields = ('customer', 'barberman', 'reserved_type',
                  'reserved_date', 'reserved_time', 'styleitem')
        extra_kwargs = {
            'barberman': {'required': True},
            'styleitem': {
                'allow_blank': True,
                'allow_null': True,
                'required': False
            },
            'reserved_type': {'required': False},
            'reserved_date': {'required': False},
            'reserved_time': {'required': False},
        }

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['reserved_date'] = timezone.datetime.today().date()
        data['reserved_time'] = timezone.datetime.today().time()
        data['status'] = Order.Status.DONE
        return data

    @transaction.atomic()
    def create(self, validated_data):
        request = self.context.get('request')
        barberman_as_user = validated_data.pop('barberman', None)

        # get branch barberman from user
        d = timezone.datetime.today()
        dnumber = d.weekday()

        try:
            barberman_in_branch = BranchBarberman.objects \
                .prefetch_related('branch', 'user') \
                .select_related('branch', 'user') \
                .get(
                    user=barberman_as_user,
                    branch__is_default=True,
                    day=dnumber,
                    is_active=True,
                    is_holiday=False
                )
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                detail=_("Barberman tidak aktif"))

        instance = Order.objects \
            .create(barberman=barberman_in_branch, **validated_data)

        if instance:
            # direct assigned to Cashier
            user = request.user
            OrderAssigned.objects.create(order=instance, cashier=user)
        return instance


class BaseOrderSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='barber_api:customer:order-detail',
                                               lookup_field='uuid', read_only=True)
    reserved_type = serializers.SerializerMethodField()
    styleitem = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    rating = RetrieveOrderRatingSerializer(read_only=True)

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


class ListOrderSerializer(BaseOrderSerializer):
    class Meta:
        model = Order
        fields = ('create_at', 'date', 'reserved_date', 'reserved_time', 'url',
                  'uuid', 'reserved_type', 'styleitem', 'status', 'status_display',
                  'note', 'rating',)


class RetrieveOrderSerializer(BaseOrderSerializer):
    attachments = OrderAttachmentSerializer(many=True)
    customer = serializers.CharField(source='customer.name')
    barberman = serializers.CharField(source='barberman.user.name')

    class Meta:
        model = Order
        fields = '__all__'


class HistoryOrderSerializer(serializers.ModelSerializer):
    attachments = OrderAttachmentSerializer(many=True)
    reserved_year = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('attachments', 'reserved_date',
                  'reserved_time', 'reserved_year',)

    def get_reserved_year(self, instante):
        return instante.reserved_date.year


class OrderAttachmentSerializer(BaseOrderSerializer):
    class Meta:
        model = OrderAttachment
        fields = ('file', 'angle',)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        order = self.context.get('order')
        data['order'] = order
        return data

    @transaction.atomic
    def create(self, validated_data):
        file = validated_data.get('file')
        instance = OrderAttachment.objects.create(
            filesize=file.size, **validated_data)
        handle_upload_attachment(instance, file)
        return instance
