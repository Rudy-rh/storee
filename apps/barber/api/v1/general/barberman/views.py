from django.utils import timezone
from rest_framework import viewsets, status as status_code
from rest_framework.response import Response

from utils.generals import get_model
from .serializers import BarbermanSerializer

BranchBarberman = get_model('barber', 'BranchBarberman')


class BarbermanApiView(viewsets.ViewSet):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._context = {}

    def dispatch(self, request, *args, **kwargs):
        self._context.update({'request': request})
        return super().dispatch(request, *args, **kwargs)

    def _get_instances(self):
        d = timezone.datetime.today()
        dnumber = d.weekday()

        return BranchBarberman.objects \
            .prefetch_related('branch', 'user') \
            .select_related('branch', 'user') \
            .filter(
                branch__is_default=True,
                day=dnumber,
                is_active=True,
                is_holiday=False
            )

    def list(self, request, format='json'):
        instances = self._get_instances()
        serializer = BarbermanSerializer(instances, many=True,
                                         context=self._context)
        return Response({'results': serializer.data}, status=status_code.HTTP_200_OK)
