from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .abstract import AbstractCommonField


class AbstractBooking(AbstractCommonField):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='bookings')
    barberman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  null=True, limit_choices_to={'groups__name': 'Barberman'})

    reserved_date = models.DateField(auto_now=False)
    reserved_time = models.TimeField(auto_now=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'barber'
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
