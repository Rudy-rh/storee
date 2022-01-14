from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.apps import apps
from django.db.models import Avg, Count
from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model
from django.core.serializers import serialize

User = get_user_model()
OrderRating = apps.get_registered_model('barber', 'OrderRating')


class StatView(View):
    template_name = 'admin/stat.html'

    def get(self, request):
        data = {}
        barberman_ratings_json = []
        until_date = timezone.datetime(2021, 11, 1)

        rating = OrderRating.objects \
            .aggregate(
                total=Count('id'),
                rmanagement=Avg('rmanagement'),
                rhygiene=Avg('rhygiene'),
                rbarberman=Avg('rbarberman'),
                rcashier=Avg('rcashier'),
                rsuggestion=Avg('rsuggestion')
            )

        barberman_ratings = User.objects \
            .annotate(
                total_order=Count(
                    'barbermans__orders__rating',
                    filter=Q(
                        barbermans__orders__rating__create_at__gte=until_date
                    )
                ),
                rating_average=Avg(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(
                        barbermans__orders__rating__create_at__gte=until_date
                    )
                ),

                star_1_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(
                        barbermans__orders__rating__rbarberman=1,
                        barbermans__orders__rating__create_at__gte=until_date
                    )
                ),
                star_2_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(
                        barbermans__orders__rating__rbarberman=2,
                        barbermans__orders__rating__create_at__gte=until_date
                    )
                ),
                star_3_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(
                        barbermans__orders__rating__rbarberman=3,
                        barbermans__orders__rating__create_at__gte=until_date
                    )
                ),
                star_4_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(
                        barbermans__orders__rating__rbarberman=4,
                        barbermans__orders__rating__create_at__gte=until_date
                    )
                ),
                star_5_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(
                        barbermans__orders__rating__rbarberman=5,
                        barbermans__orders__rating__create_at__gte=until_date
                    )
                )
            ) \
            .filter(
                Q(groups__name='Barberman'),
                Q(total_order__gt=0)
            ) \
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

        data.update({
            'barberman_ratings': barberman_ratings,
            'barberman_ratings_json': barberman_ratings_json,
        })

        return render(request, self.template_name, data)
