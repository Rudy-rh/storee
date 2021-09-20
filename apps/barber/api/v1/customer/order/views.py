from collections import defaultdict

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from rest_framework import viewsets, status as response_status
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from utils.generals import get_model
from utils.pagination import build_result_pagination
from .serializers import (
    CreateOrderByTakePhotoSerializer,
    CreateOrderRatingSerializer,
    CreateOrderSerializer,
    ListOrderSerializer,
    OrderAttachmentSerializer,
    RetrieveOrderRatingSerializer,
    RetrieveOrderSerializer
)

Order = get_model('barber', 'Order')
OrderAttachment = get_model('barber', 'OrderAttachment')

# Define to avoid used ...().paginate__
_PAGINATOR = LimitOffsetPagination()


class OrderApiView(viewsets.ViewSet):
    """
    GET
    -------

        ../?timelapse=<customer,today,tomorrow,all>


    POST
    -------

        Format;
        {
            "reserved_date": "2021-06-20",
            "reserved_time": "12:30",
            "reserved_type": "ms",
            "styleitem": "27a19a42-0b4f-4503-a34a-003194d41aec",
            "barberman": "db52f520-80db-4de8-8000-e9f1292d6cb7",
            "note": "Order saja..."
        }
    """

    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._context = {}
        self._uuid = None

    def dispatch(self, request, *args, **kwargs):
        self._context.update({'request': request})
        self._uuid = kwargs.get('uuid')
        return super().dispatch(request, *args, **kwargs)

    def _get_instances(self):
        return Order.objects \
            .prefetch_related('customer', 'branch', 'barberman', 'rating') \
            .select_related('customer', 'branch', 'barberman', 'rating') \
            .filter(
                Q(customer_id=self.request.user.id)
                | Q(assigned__cashier_id=self.request.user.id)
                | Q(barberman__user_id=self.request.user.id)
            )

    def _get_instance(self):
        try:
            return self._get_instances().get(uuid=self._uuid)
        except ObjectDoesNotExist:
            raise NotFound()

    def list(self, request, format='json'):
        instances = self._get_instances()
        params = request.query_params
        timelapse = params.get('timelapse')

        # as cashier see booking by date now and tomorrow
        if request.user.is_cashier:
            date = None

            if timelapse == 'today' or timelapse == 'customer':
                year = timezone.datetime.today().year
                month = timezone.datetime.today().month
                day = timezone.datetime.today().day
                date = timezone.datetime(year, month, day)
                if timelapse == 'today':
                    instances = instances.filter(is_booking=True)
                elif timelapse == 'customer':
                    # all customer booking or not
                    instances = instances.filter(is_booking=False)
            elif timelapse == 'tomorrow':
                tomorrow = timezone.datetime.today() + timezone.timedelta(days=1)
                year = tomorrow.year
                month = tomorrow.month
                day = tomorrow.day
                date = timezone.datetime(year, month, day)
                instances = instances.filter(is_booking=True)

            if date:
                instances = instances.filter(reserved_date=date)

        # as barberman
        if request.user.is_barberman:
            instances = instances.filter(is_booking=True)

        paginator = _PAGINATOR.paginate_queryset(instances, request)
        serializer = ListOrderSerializer(paginator, context=self._context,
                                         many=True)
        results = build_result_pagination(self, _PAGINATOR, serializer)
        return Response(results, status=response_status.HTTP_200_OK)

    def retrieve(self, request, uuid=None, format=None):
        instance = self._get_instance()
        serializer = RetrieveOrderSerializer(instance, many=False,
                                             context=self._context)
        return Response({'result': serializer.data}, status=response_status.HTTP_200_OK)

    @transaction.atomic()
    def create(self, request, format='json'):
        serializer = CreateOrderSerializer(data=request.data, context=self._context,
                                           many=False)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except ValidationError as e:
                raise ValidationError({'detail': str(e)})

            _serializer = RetrieveOrderSerializer(serializer.instance, many=False,
                                                  context=self._context)
            return Response(_serializer.data, status=response_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=response_status.HTTP_406_NOT_ACCEPTABLE)

    @transaction.atomic()
    @action(detail=True, methods=['post'], url_name='rating', url_path='rating')
    def rating(self, request, uuid=None, format='json'):
        """
        POST
        --------------

        Format;

            {
                "rmanagement": "integer 1 - 5",
                "rhygiene": "integer 1 - 5",
                "rbarberman": "integer 1 - 5",
                "rcashier": "integer 1 - 5",
                "rsuggestion": "text"
            }
        """
        instance = self._get_instance()
        self._context.update({'order': instance})
        serializer = CreateOrderRatingSerializer(data=request.data, context=self._context,
                                                 many=False)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except ValidationError as e:
                raise ValidationError({'detail': str(e)})

            _serializer = RetrieveOrderRatingSerializer(serializer.instance, many=False,
                                                        context=self._context)
            return Response(_serializer.data, status=response_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=response_status.HTTP_406_NOT_ACCEPTABLE)

    # create order by cashier
    @transaction.atomic()
    @action(detail=False, methods=['post'], url_name='take_order', url_path='take-order')
    def take_order(self, request, format='json'):
        """
        POST;
        -------
            Format;
            {
                "styleitem": "27a19a42-0b4f-4503-a34a-003194d41aec",
                "barberman": "username",
                "customer": "username"
            }
        """

        serializer = CreateOrderByTakePhotoSerializer(data=request.data, context=self._context,
                                                      many=False)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except ValidationError as e:
                raise ValidationError({'detail': str(e)})

            _serializer = RetrieveOrderSerializer(serializer.instance, many=False,
                                                  context=self._context)
            return Response(_serializer.data, status=response_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=response_status.HTTP_406_NOT_ACCEPTABLE)

    @transaction.atomic()
    @action(detail=True, methods=['post'], url_name='attachment', url_path='attachments',
            parser_classes=[MultiPartParser])
    def attachment(self, request, uuid=None, format=None):
        """
        Format;

            {
                "file": "file object"
            }
        """
        order = self._get_instance()
        self._context.update({'order': order})
        serializer = OrderAttachmentSerializer(data=request.data, many=False,
                                               context=self._context)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except ValidationError as e:
                raise ValidationError({'detail': str(e)})

            _serializer = RetrieveOrderSerializer(serializer.instance.order, many=False,
                                                  context=self._context)
            return Response(_serializer.data, status=response_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=response_status.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=False, methods=['get'], url_name='history', url_path='histories')
    def history(self, request, format=None):
        year = request.query_params.get('year', None)
        if not year:
            raise NotAcceptable(detail=_("Year not defined"))

        attachments = OrderAttachment.objects \
            .prefetch_related('order') \
            .select_related('order') \
            .filter(
                Q(order__reserved_date__year=year),
                Q(order__customer_id=request.user.id)
                | Q(order__barberman__user_id=request.user.id)
            )

        tmp = defaultdict(list)
        for item in attachments:
            d = item.order.reserved_date.strftime("%Y-%m")
            image = request.build_absolute_uri(item.file.url)
            tmp[d].append([image])

        parsed_list = [
            {
                'date': k,
                'year': timezone.datetime.strptime(k, "%Y-%m").year,
                'files': v
            } for k, v in tmp.items()
        ]

        return Response(parsed_list, status=response_status.HTTP_200_OK)
