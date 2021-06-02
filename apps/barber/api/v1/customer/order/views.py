from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status as status_code
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser

from utils.generals import get_model
from utils.pagination import build_result_pagination
from .serializers import (
    CreateOrderByTakePhotoSerializer,
    CreateOrderRatingSerializer,
    CreateOrderSerializer,
    HistoryOrderSerializer,
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
    POST;
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
        self._user = None
        self._uuid = None

    def dispatch(self, request, *args, **kwargs):
        self._context.update({'request': request})
        self._uuid = kwargs.get('uuid')
        return super().dispatch(request, *args, **kwargs)

    def _get_instances(self):
        return Order.objects \
            .prefetch_related('customer', 'branch', 'barberman', 'rating') \
            .select_related('customer', 'branch', 'barberman', 'rating') \
            .filter(Q(customer_id=self._user.id) | Q(assigned__cashier_id=self._user.id))

    def _get_instance(self):
        try:
            return self._get_instances().get(uuid=self._uuid)
        except ObjectDoesNotExist:
            raise NotFound()

    def list(self, request, format='json'):
        self._user = request.user
        instances = self._get_instances()
        paginator = _PAGINATOR.paginate_queryset(instances, request)
        serializer = ListOrderSerializer(paginator, context=self._context,
                                         many=True)
        results = build_result_pagination(self, _PAGINATOR, serializer)
        return Response(results, status=status_code.HTTP_200_OK)

    def retrieve(self, request, uuid=None, format=None):
        self._user = request.user
        instance = self._get_instance()
        serializer = RetrieveOrderSerializer(instance, many=False,
                                             context=self._context)
        return Response({'result': serializer.data}, status=status_code.HTTP_200_OK)

    @transaction.atomic()
    def create(self, request, format='json'):
        self._user = request.user
        serializer = CreateOrderSerializer(data=request.data, context=self._context,
                                           many=False)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except ValidationError as e:
                raise ValidationError({'detail': str(e)})

            _serializer = RetrieveOrderSerializer(serializer.instance, many=False,
                                                  context=self._context)
            return Response(_serializer.data, status=status_code.HTTP_201_CREATED)
        return Response(serializer.errors, status=status_code.HTTP_406_NOT_ACCEPTABLE)

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
        self._user = request.user
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
            return Response(_serializer.data, status=status_code.HTTP_201_CREATED)
        return Response(serializer.errors, status=status_code.HTTP_406_NOT_ACCEPTABLE)

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
            return Response(_serializer.data, status=status_code.HTTP_201_CREATED)
        return Response(serializer.errors, status=status_code.HTTP_406_NOT_ACCEPTABLE)

    @transaction.atomic()
    @action(detail=True, methods=['post'], url_name='attachment', url_path='attachments',
            permission_classes=[IsAuthenticated], parser_classes=[FileUploadParser])
    def attachment(self, request, uuid=None, format=None):
        """
        Format;

            {
                "file": "file object"
            }
        """
        self._user = request.user
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
            return Response(_serializer.data, status=status_code.HTTP_201_CREATED)
        return Response(serializer.errors, status=status_code.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=False, methods=['get'], url_name='history', url_path='histories')
    def history(self, request, format=None):
        year = request.query_params.get('year', None)
        if not year:
            raise NotAcceptable(detail=_("Year not defined"))

        attachments = Order.objects \
            .prefetch_related('customer', 'attachments') \
            .select_related('customer') \
            .filter(reserved_date__year=year, customer_id=request.user.id)

        serializer = HistoryOrderSerializer(
            attachments, many=True, context=self._context)
        return Response(serializer.data, status=status_code.HTTP_200_OK)
