from tokenize import group
from django.views.generic.list import ListView
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.apps import apps
from django.db.models import Avg, Count
from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model

User = get_user_model()
OrderRating = apps.get_registered_model('barber', 'OrderRating')


class StatView(View):
    template_name = 'admin/stat.html'

    def get(self, request):
        data = {}
        barberman_ratings_json = []
        cashier_ratings_json = []
        until_date = timezone.datetime(2021, 11, 1)

        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        is_filtered = start_date and end_date
        rating_overall_qs = OrderRating.objects

        if not is_filtered:
            rating_overall_qs = rating_overall_qs \
                .filter(create_at__gte=until_date)
        else:
            start_date_obj = timezone.datetime.strptime(start_date, '%d/%m/%Y')
            end_date_obj = timezone.datetime.strptime(end_date, '%d/%m/%Y')

            rating_overall_qs = rating_overall_qs \
                .filter(create_at__range=(start_date_obj, end_date_obj))

        rating_overall = rating_overall_qs.aggregate(
                total=Count('id'),
                rmanagement=Avg('rmanagement'),
                rhygiene=Avg('rhygiene'),
                rbarberman=Avg('rbarberman'),
                rcashier=Avg('rcashier'),
                rsuggestion=Avg('rsuggestion')
            )

        # filtered by date
        if is_filtered:
            barberman_q = Q(
                barbermans__orders__rating__create_at__range=(
                    start_date_obj, end_date_obj)
            )
        else:
            barberman_q = Q(
                barbermans__orders__rating__create_at__gte=until_date)

        barberman_ratings = User.objects \
            .annotate(
                total_order=Count(
                    'barbermans__orders__rating',
                    filter=barberman_q
                ),
                rating_average=Avg(
                    'barbermans__orders__rating__rbarberman',
                    filter=barberman_q
                ),
                star_1_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(
                        barbermans__orders__rating__rbarberman=1) & barberman_q
                ),
                star_2_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(
                        barbermans__orders__rating__rbarberman=2) & barberman_q
                ),
                star_3_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(
                        barbermans__orders__rating__rbarberman=3) & barberman_q
                ),
                star_4_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(
                        barbermans__orders__rating__rbarberman=4) & barberman_q
                ),
                star_5_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(
                        barbermans__orders__rating__rbarberman=5) & barberman_q
                )
            ) \
            .filter(Q(groups__name='Barberman'), Q(total_order__gt=0)) \
            .order_by('-id')

        for d in barberman_ratings:
            x = {
                'total_order': d.total_order,
                'rating_average': d.rating_average,
                'star_1_count': d.star_1_count,
                'star_2_count': d.star_2_count,
                'star_3_count': d.star_3_count,
                'star_4_count': d.star_4_count,
                'star_5_count': d.star_5_count,
                'name': d.name,
                'id': d.id,
            }

            barberman_ratings_json.append(x)

        # filtered by date
        if is_filtered:
            cashier_q = Q(
                assigneds__rating__create_at__range=(
                    start_date_obj, end_date_obj)
            )
        else:
            cashier_q = Q(assigneds__rating__create_at__gte=until_date)

        cashier_ratings = User.objects \
            .annotate(
                total_order=Count(
                    'assigneds__rating',
                    filter=cashier_q
                ),
                rating_average=Avg(
                    'assigneds__rating__rcashier',
                    filter=cashier_q
                ),
                star_1_count=Count(
                    'assigneds__rating__rcashier',
                    filter=Q(assigneds__rating__rcashier=1) & cashier_q
                ),
                star_2_count=Count(
                    'assigneds__rating__rcashier',
                    filter=Q(assigneds__rating__rcashier=2) & cashier_q
                ),
                star_3_count=Count(
                    'assigneds__rating__rcashier',
                    filter=Q(assigneds__rating__rcashier=3) & cashier_q
                ),
                star_4_count=Count(
                    'assigneds__rating__rcashier',
                    filter=Q(assigneds__rating__rcashier=4) & cashier_q
                ),
                star_5_count=Count(
                    'assigneds__rating__rcashier',
                    filter=Q(assigneds__rating__rcashier=5) & cashier_q
                )
            ) \
            .filter(Q(groups__name='Cashier'), Q(total_order__gt=0)) \
            .order_by('-id')

        for d in cashier_ratings:
            x = {
                'total_order': d.total_order,
                'rating_average': d.rating_average,
                'star_1_count': d.star_1_count,
                'star_2_count': d.star_2_count,
                'star_3_count': d.star_3_count,
                'star_4_count': d.star_4_count,
                'star_5_count': d.star_5_count,
                'name': d.name,
                'id': d.id,
            }

            cashier_ratings_json.append(x)

        data.update({
            'barberman_ratings': barberman_ratings,
            'barberman_ratings_json': barberman_ratings_json,
            'cashier_ratings': cashier_ratings,
            'cashier_ratings_json': cashier_ratings_json,
            'rating_overall_json': rating_overall,
            'is_filtered': is_filtered,
        })

        return render(request, self.template_name, data)


class RatingListView(ListView):
    model = OrderRating
    paginate_by = 25
    template_name = 'admin/rating.html'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        qs = super().get_queryset() \
            .prefetch_related('order') \
            .select_related('order')

        if user_id:
            qs = qs.prefetch_related('order', 'order__barberman', 'assigned') \
                .select_related('order', 'order__barberman', 'assigned') \
                .filter(
                    Q(assigned__cashier__id=user_id) |
                    Q(order__barberman__user__id=user_id)
            )

        return qs

    def get_context_data(self, **kwargs):
        user_id = self.kwargs.get('user_id')
        name = None
        is_barberman = False
        is_cashier = False

        if user_id:
            user = User.objects.filter(id=user_id)
            name = user.get().name
            is_barberman = user.filter(groups__name='Barberman').exists()
            is_cashier = user.filter(groups__name='Cashier').exists()

        context = super().get_context_data(**kwargs)
        context['name'] = name
        context['total'] = self.get_queryset().count()
        context['is_barberman'] = is_barberman
        context['is_cashier'] = is_cashier

        return context
