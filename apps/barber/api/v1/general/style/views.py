from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status as response_status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from utils.generals import get_model
from .serializers import ListStyleOfTheYearSerializer, ListStyleSerializer, RetrieveStyleSerializer

StyleCategory = get_model('barber', 'StyleCategory')
StyleOfTheYear = get_model('barber', 'StyleOfTheYear')


class StyleApiView(viewsets.ViewSet):
    lookup_field = 'uuid'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._context = {}
        self._uuid = None

    def dispatch(self, request, *args, **kwargs):
        self._context.update({'request': request})
        self._uuid = kwargs.get('uuid')
        return super().dispatch(request, *args, **kwargs)

    def _get_instances(self):
        return StyleCategory.objects \
            .prefetch_related('items', 'items__attachments') \
            .all()

    def _get_instance(self):
        return self._get_instances().get(uuid=self._uuid)

    def list(self, request, format='json'):
        instances = self._get_instances()
        serializer = ListStyleSerializer(instances, many=True,
                                         context=self._context)
        return Response({'results': serializer.data}, status=response_status.HTTP_200_OK)

    def retrieve(self, request, uuid=None, format=None):
        try:
            instance = self._get_instance()
        except ObjectDoesNotExist:
            raise NotFound()

        serializer = RetrieveStyleSerializer(instance, many=False,
                                             context=self._context)
        return Response({'result': serializer.data}, status=response_status.HTTP_200_OK)


class StyleOfTheYearApiView(viewsets.ViewSet):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._context = {}

    def dispatch(self, request, *args, **kwargs):
        self._context.update({'request': request})
        return super().dispatch(request, *args, **kwargs)

    def _get_instances(self):
        return StyleOfTheYear.objects.all()[:30]

    def list(self, request, format='json'):
        instances = self._get_instances()
        serializer = ListStyleOfTheYearSerializer(instances, many=True,
                                                  context=self._context)
        return Response({'results': serializer.data}, status=response_status.HTTP_200_OK)
