from django.shortcuts import render
from django.views import View
from django.apps import apps
from django.db.models import Avg, Count
from django.contrib.auth import get_user_model

User = get_user_model()
OrderRating = apps.get_registered_model('barber', 'OrderRating')


class StatView(View):
    template_name = 'admin/stat.html'

    def get(self, request):
        data = {}
        rating = OrderRating.objects \
            .aggregate(
                total=Count('id'),
                rmanagement=Avg('rmanagement'),
                rhygiene=Avg('rhygiene'),
                rbarberman=Avg('rbarberman'),
                rcashier=Avg('rcashier'),
                rsuggestion=Avg('rsuggestion')
            )

        print(rating)

        barberman = User.objects.filter(groups__name='Barberman')

        print(barberman)

        return render(request, self.template_name, data)
