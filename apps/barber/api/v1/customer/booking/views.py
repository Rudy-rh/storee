from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets, status as status_code
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from utils.generals import get_model
from utils.pagination import build_result_pagination
from .serializers import CreateBookingSerializer, ListBookingSerializer, RetrieveBookingSerializer

Booking = get_model('barber', 'Booking')

# Define to avoid used ...().paginate__
_PAGINATOR = LimitOffsetPagination()


class BookingApiView(viewsets.ViewSet):
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
            "note": "Booking saja..."
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
        self._user = request.user
        self._uuid = kwargs.get('uuid')
        return super().dispatch(request, *args, **kwargs)

    def _get_instances(self):
        return Booking.objects \
            .prefetch_related('customer', 'branch', 'barberman') \
            .select_related('customer', 'branch', 'barberman') \
            .filter(customer=self._user.id)

    def _get_instance(self):
        return self._get_instances().get(uuid=self._uuid)

    def list(self, request, format='json'):
        instances = self._get_instances()
        paginator = _PAGINATOR.paginate_queryset(instances, request)
        serializer = ListBookingSerializer(paginator, context=self._context,
                                           many=True)
        results = build_result_pagination(self, _PAGINATOR, serializer)
        return Response(results, status=status_code.HTTP_200_OK)

    def retrieve(self, request, uuid=None, format=None):
        try:
            instance = self._get_instance()
        except ObjectDoesNotExist:
            raise NotFound()

        serializer = RetrieveBookingSerializer(instance, many=False,
                                               context=self._context)
        return Response({'result': serializer.data}, status=status_code.HTTP_200_OK)

    @transaction.atomic()
    def create(self, request, format='json'):
        serializer = CreateBookingSerializer(data=request.data, context=self._context,
                                             many=False)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except ValidationError as e:
                raise ValidationError({'detail': str(e)})

            _serializer = RetrieveBookingSerializer(serializer.instance, many=False,
                                                    context=self._context)
            return Response(_serializer.data, status=status_code.HTTP_201_CREATED)
        return Response(serializer.errors, status=status_code.HTTP_406_NOT_ACCEPTABLE)
