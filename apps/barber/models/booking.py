from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

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

    class Status(models.TextChoices):
        PENDING = 'pending', _("Pending")
        ACCEPT = 'accept', _("Accept")
        REJECT = 'reject', _("Reject")
        DONE = 'done', _("Done")

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='bookings', limit_choices_to={'groups__name': 'Customer'})
    styleitem = models.ForeignKey('barber.StyleItem', on_delete=models.CASCADE,
                                  related_name='bookings', null=True, blank=True)
    barberman = models.ForeignKey('barber.BranchBarberman', on_delete=models.SET_NULL,
                                  null=True, limit_choices_to={'user__groups__name': 'Barberman'})
    branch = models.ForeignKey('barber.Branch', on_delete=models.CASCADE,
                               related_name='bookings', editable=False)

    reserved_type = models.CharField(choices=Types.choices, max_length=5)
    reserved_date = models.DateField(auto_now=False)
    reserved_time = models.TimeField(auto_now=True)
    note = models.TextField(null=True, blank=True)
    status = models.CharField(choices=Status.choices, default=Status.PENDING,
                              max_length=15)

    class Meta:
        abstract = True
        app_label = 'barber'
        ordering = ['-create_at']
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")

    def __str__(self):
        return self.customer.name

    def save(self, *args, **kwargs):
        # save branch from barberman
        branch = self.barberman.branch
        if branch:
            self.branch = branch
        return super().save(*args, **kwargs)


class AbstractBookingAssigned(AbstractCommonField):
    booking = models.OneToOneField('barber.Booking', on_delete=models.CASCADE,
                                   related_name='assigned')
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='assigneds', limit_choices_to={'groups__name': 'Cashier'})

    class Meta:
        abstract = True
        app_label = 'barber'
        ordering = ['-create_at']
        verbose_name = _("Booking Assigned")
        verbose_name_plural = _("Booking Assigneds")

    def __str__(self):
        return self.cashier.name


class AbstractBookingRating(AbstractCommonField):
    """ Each Booking only has one time rating """
    class Star(models.IntegerChoices):
        S1 = 1, _("1 Star")
        S2 = 2, _("2 Stars")
        S3 = 3, _("3 Stars")
        S4 = 4, _("4 Stars")
        S5 = 5, _("5 Stars")

    booking = models.OneToOneField('barber.Booking', on_delete=models.CASCADE,
                                   related_name='rating')
    assigned = models.OneToOneField('barber.BookingAssigned', on_delete=models.CASCADE,
                                    related_name='rating', editable=False)

    rmanagement = models.IntegerField(choices=Star.choices,
                                      validators=[MaxValueValidator(5), MinValueValidator(1)])
    rhygiene = models.IntegerField(choices=Star.choices,
                                   validators=[MaxValueValidator(5), MinValueValidator(1)])
    rbarberman = models.IntegerField(choices=Star.choices,
                                     validators=[MaxValueValidator(5), MinValueValidator(1)])
    rcashier = models.IntegerField(choices=Star.choices,
                                   validators=[MaxValueValidator(5), MinValueValidator(1)])
    rsuggestion = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'barber'
        ordering = ['-create_at']
        verbose_name = _("Booking Rating")
        verbose_name_plural = _("Booking Ratings")

    def __str__(self):
        return self.booking.customer.username

    def save(self, *args, **kwargs):
        self.assigned = self.booking.assigned
        super().save(*args, **kwargs)
