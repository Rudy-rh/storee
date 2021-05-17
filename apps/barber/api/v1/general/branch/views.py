from rest_framework import viewsets, status as response_status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.generals import get_model
from .serializers import BranchSerializer

Branch = get_model('barber', 'Branch')


class BranchApiView(viewsets.ViewSet):
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)

    def list(self, request, format='json'):
        context = {'request': request}
        instances = Branch.objects.all()
        serializer = BranchSerializer(instances, many=True, context=context)
        return Response(serializer.data, status=response_status.HTTP_200_OK)
