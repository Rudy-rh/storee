from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .abstract import AbstractCommonField


class AbstractBooking(AbstractCommonField):
    class Types(models.TextChoices):
        HAIRCUT = 'hc', _("Hair Cut")
        HAIRSPA = 'hs', _("Hair Spa")
        MESSAGE = 'ms', _("Message")
        COLORING = 'cr', _("Coloring")
        BLACKMASK = 'bm', _("Black Mask")
        OZONE_MICROMIST = 'om', _("Ozone MicroMist"),
        OTHER = 'ot', _("Lainnya")

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='bookings', limit_choices_to={'groups__name': 'Customer'})
    barberman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  null=True, limit_choices_to={'groups__name': 'Barberman'})

    reserved_type = models.CharField(choices=Types.choices, max_length=5)
    reserved_date = models.DateField(auto_now=False)
    reserved_time = models.TimeField(auto_now=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'barber'
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
