from decimal import Decimal
from django.conf import settings

from django.db import models
from .abstract import AbstractCommonField


class AbstractBranch(AbstractCommonField):
    name = models.CharField(max_length=255, db_index=True)
    address = models.TextField()
    icon = models.ImageField(upload_to='branch', null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   default=Decimal(0.0), db_index=True,
                                   null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    default=Decimal(0.0), db_index=True,
                                    null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'barber'

    def __str__(self) -> str:
        return self.name


class AbstractBranchBarberman(AbstractCommonField):
    branch = models.ForeignKey('barber.Branch', on_delete=models.CASCADE,
                               related_name='barbermans')
    barberman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='barbermans',
                                  limit_choices_to={'groups__name': 'Barberman'})
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        app_label = 'barber'


class AbstractBranchCashier(AbstractCommonField):
    branch = models.ForeignKey('barber.Branch', on_delete=models.CASCADE,
                               related_name='cashiers')
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='cashiers',
                                limit_choices_to={'groups__name': 'Cashier'})
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        app_label = 'barber'
