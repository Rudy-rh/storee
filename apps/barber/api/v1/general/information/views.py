from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status as response_status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.generals import get_model
from .serializers import InformationSerializer

Information = get_model('barber', 'Information')


class InformationApiView(viewsets.ViewSet):
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        context = {'request': request}
        instances = Information.objects \
            .prefetch_related('informations_read') \
            .exclude(informations_read__user_id=request.user.id)

        serializer = InformationSerializer(
            instances, context=context, many=True)
        return Response(serializer.data, status=response_status.HTTP_200_OK)

    def retrieve(self, request, uuid, format='json'):
        context = {'request': request}

        try:
            instance = Information.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            raise NotFound()

        serializer = InformationSerializer(instance, context=context)
        return Response(serializer.data, status=response_status.HTTP_200_OK)
