from decimal import Decimal

from django.conf import settings
from django.utils.translation import gettext_lazy as _
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
    is_default = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'barber'

    def __str__(self) -> str:
        return self.name


class AbstractBranchBarberman(AbstractCommonField):
    class Day(models.IntegerChoices):
        MO = 0, _("Monday")
        TU = 1, _("Tuesday")
        WE = 2, _("Wednesday")
        TH = 3, _("Thursday")
        FR = 4, _("Friday")
        SA = 5, _("Saturday")
        SU = 6, _("Sunday")

    branch = models.ForeignKey('barber.Branch', on_delete=models.CASCADE,
                               related_name='barbermans')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='barbermans',
                             limit_choices_to={'groups__name': 'Barberman'})

    day = models.IntegerField(choices=Day.choices)
    start_hour = models.TimeField(blank=True, null=True)
    end_hour = models.TimeField(blank=True, null=True)
    is_holiday = models.BooleanField(default=False)
    is_weekend = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'barber'

    def __str__(self) -> str:
        return self.user.name


class AbstractBranchCashier(AbstractCommonField):
    class Day(models.IntegerChoices):
        MO = 0, _("Monday")
        TU = 1, _("Tuesday")
        WE = 2, _("Wednesday")
        TH = 3, _("Thursday")
        FR = 4, _("Friday")
        SA = 5, _("Saturday")
        SU = 6, _("Sunday")

    branch = models.ForeignKey('barber.Branch', on_delete=models.CASCADE,
                               related_name='cashiers')
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='cashiers',
                                limit_choices_to={'groups__name': 'Cashier'})

    day = models.IntegerField(choices=Day.choices)
    start_hour = models.TimeField(blank=True, null=True)
    end_hour = models.TimeField(blank=True, null=True)
    is_holiday = models.BooleanField(default=False)
    is_weekend = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'barber'

    def __str__(self) -> str:
        return self.cashier.name
