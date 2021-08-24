from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status as response_status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.generals import get_model
from .serializers import BannerSerializer

Banner = get_model('barber', 'Banner')


class BannerApiView(viewsets.ViewSet):
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        context = {'request': request}
        instances = Banner.objects \
            .filter(is_active=True) \
            .order_by('-position')

        serializer = BannerSerializer(instances, context=context, many=True)
        return Response(serializer.data, status=response_status.HTTP_200_OK)

    def retrieve(self, request, uuid, format='json'):
        context = {'request': request}

        try:
            instance = Banner.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            raise NotFound()

        serializer = BannerSerializer(instance, context=context)
        return Response(serializer.data, status=response_status.HTTP_200_OK)
