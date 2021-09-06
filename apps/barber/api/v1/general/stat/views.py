from django.apps import apps

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

Information = apps.get_registered_model('barber', 'Information')


class StatAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        information = Information.objects \
            .prefetch_related('informations_read', 'informations_read__user') \
            .exclude(informations_read__user_id=request.user.id)

        return Response({
            'count': {
                'information': information.count(),
            }
        })
