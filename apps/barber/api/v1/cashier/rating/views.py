from django.db.models.aggregates import Count, Sum
from django.db.models.query_utils import Q
from django.db.models.functions import Round
from django.utils import timezone

from rest_framework import viewsets, status as response_status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Avg, F

from .serializers import OrderRatingSerializer
from utils.generals import get_model
from utils.pagination import build_result_pagination

OrderRating = get_model('barber', 'OrderRating')

# Define to avoid used ...().paginate__
_PAGINATOR = LimitOffsetPagination()


class OrderRatingApiView(viewsets.ViewSet):
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)

    def list(self, request, format='json'):
        context = {'request': request}
        user = request.user
        until_date = timezone.datetime(2021, 11, 1)

        instances = OrderRating.objects \
            .prefetch_related('assigned', 'assigned__cashier', 'order',
                              'order__customer', 'order__barberman', 'order__barberman__user') \
            .select_related('assigned', 'assigned__cashier', 'order',
                            'order__customer', 'order__barberman', 'order__barberman__user') \
            .filter(
                Q(assigned__cashier_id=user.id)
                | Q(order__barberman__user_id=user.id),
                Q(create_at__gte=until_date)
            )

        # average
        average = instances.filter(order__status='done').aggregate(
            avg_rmanagement=Avg('rmanagement'),
            avg_rhygiene=Avg('rhygiene'),
            avg_rcashier=Avg('rcashier'),
            avg_rbarberman=Avg('rbarberman'),

            cashier_star_count=Count('rcashier'),
            cashier_star_1_count=Count('rcashier', filter=Q(rcashier=1)),
            cashier_star_2_count=Count('rcashier', filter=Q(rcashier=2)),
            cashier_star_3_count=Count('rcashier', filter=Q(rcashier=3)),
            cashier_star_4_count=Count('rcashier', filter=Q(rcashier=4)),
            cashier_star_5_count=Count('rcashier', filter=Q(rcashier=5))
        )

        paginator = _PAGINATOR.paginate_queryset(instances, request)
        serializer = OrderRatingSerializer(
            paginator, context=context, many=True)
        results = build_result_pagination(self, _PAGINATOR, serializer)
        results.update({'average': average})
        return Response(results, status=response_status.HTTP_200_OK)
