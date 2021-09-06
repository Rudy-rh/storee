from django.core.exceptions import ObjectDoesNotExist, ValidationError as DjangoValidationError

from rest_framework import viewsets, status as response_status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.generals import get_model
from .serializers import InformationSerializer, MarkReadInformationSerializer

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

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path='mark-read'
    )
    def mark_read(self, request, uuid=None, format=None):
        context = {'request': request}

        serializer = MarkReadInformationSerializer(
            data=request.data,
            many=False,
            context=context
        )

        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except DjangoValidationError as e:
                raise ValidationError({'detail': str(e)})
            return Response(serializer.data, status=response_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=response_status.HTTP_406_NOT_ACCEPTABLE)
