from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group

from rest_framework import viewsets, status as response_status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.generals import get_model
from .serializers import GroupSerializer, WorkStandardCategorySerializer

WorkStandardCategory = get_model('barber', 'WorkStandardCategory')


class GroupApiView(viewsets.ViewSet):
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        context = {'request': request}
        instances = Group.objects.filter(standard_categories__isnull=False) \
            .distinct()

        serializer = GroupSerializer(instances, context=context, many=True)
        return Response(serializer.data, status=response_status.HTTP_200_OK)

    def retrieve(self, request, id, format='json'):
        context = {'request': request}
        categories = WorkStandardCategory.objects \
            .filter(groups__id=id)
        serializer = WorkStandardCategorySerializer(categories, many=True,
                                                    context=context)
        return Response(serializer.data, status=response_status.HTTP_200_OK)
