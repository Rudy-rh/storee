from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status as response_status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.generals import get_model
from .serializers import RulesSerializer

Rules = get_model('barber', 'Rules')


class RulesApiView(viewsets.ViewSet):
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        context = {'request': request}

        try:
            instance = Rules.objects.get(is_active=True)
        except ObjectDoesNotExist:
            raise NotFound()

        serializer = RulesSerializer(instance, context=context, many=False)
        return Response(serializer.data, status=response_status.HTTP_200_OK)
