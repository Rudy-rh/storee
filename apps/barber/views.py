from django.shortcuts import render
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
                total_order=Count('barbermans__orders'),
                rating_average=Avg('barbermans__orders__rating__rbarberman'),

                star_1_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(barbermans__orders__rating__rbarberman=1)
                ),
                star_2_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(barbermans__orders__rating__rbarberman=2)
                ),
                star_3_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(barbermans__orders__rating__rbarberman=3)
                ),
                star_4_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(barbermans__orders__rating__rbarberman=4)
                ),
                star_5_count=Count(
                    'barbermans__orders__rating__rbarberman',
                    filter=Q(barbermans__orders__rating__rbarberman=5)
                )
            ) \
            .filter(groups__name='Barberman') \
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
