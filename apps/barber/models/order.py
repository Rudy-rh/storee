from datetime import timedelta
import os

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.person.tasks import send_thanks_to_customer_whatsapp, add

from .abstract import AbstractCommonField


def censort(t):
    appear = t[-3:]
    size = len(t)
    censored = t[:size - 3]
    word = '*' * len(censored)
    return word + appear


class AbstractOrder(AbstractCommonField):
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
                                 related_name='orders', limit_choices_to={'groups__name': 'Customer'})
    styleitem = models.ForeignKey('barber.StyleItem', on_delete=models.CASCADE,
                                  related_name='orders', null=True, blank=True)
    barberman = models.ForeignKey('barber.BranchBarberman', on_delete=models.SET_NULL, blank=True,
                                  null=True, limit_choices_to={'user__groups__name': 'Barberman'})
    branch = models.ForeignKey('barber.Branch', on_delete=models.SET_NULL,
                               related_name='orders', editable=False, null=True, blank=True)

    reserved_type = models.CharField(choices=Types.choices, max_length=5)
    reserved_date = models.DateField(auto_now=False)
    reserved_time = models.TimeField(auto_now=False)
    note = models.TextField(null=True, blank=True)
    status = models.CharField(choices=Status.choices, default=Status.PENDING,
                              max_length=15)
    is_booking = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'barber'
        ordering = ['-create_at']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return self.customer.name

    def save(self, *args, **kwargs):
        # save branch from barberman
        if self.barberman:
            branch = self.barberman.branch
            if branch:
                self.branch = branch

        """
        msisdn = '0811806807'
        send_date = timezone.datetime.today() + timedelta(seconds=30)
        send_thanks_to_customer_whatsapp.apply_async([msisdn,], countdown=5)
        """

        return super().save(*args, **kwargs)

    @property
    def reserved_time_fmt(self):
        return self.reserved_time.strftime('%H:%M')


class AbstractOrderAssigned(AbstractCommonField):
    order = models.OneToOneField('barber.Order', on_delete=models.CASCADE,
                                 related_name='assigned')
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='assigneds', limit_choices_to={'groups__name': 'Cashier'})

    class Meta:
        abstract = True
        app_label = 'barber'
        ordering = ['-create_at']
        verbose_name = _("Order Assigned")
        verbose_name_plural = _("Order Assigneds")

    def __str__(self):
        return self.cashier.name


class AbstractOrderRating(AbstractCommonField):
    """ Each Order only has one time rating """
    class Star(models.IntegerChoices):
        S1 = 1, _("1 Star")
        S2 = 2, _("2 Stars")
        S3 = 3, _("3 Stars")
        S4 = 4, _("4 Stars")
        S5 = 5, _("5 Stars")

    order = models.OneToOneField('barber.Order', on_delete=models.CASCADE,
                                 related_name='rating')
    assigned = models.OneToOneField('barber.OrderAssigned', on_delete=models.CASCADE,
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
        verbose_name = _("Order Rating")
        verbose_name_plural = _("Order Ratings")

    def __str__(self):
        return self.order.customer.username

    @property
    def customer(self):
        t = self.order.customer.username
        c = censort(t)
        return c

    def save(self, *args, **kwargs):
        self.assigned = self.order.assigned
        super().save(*args, **kwargs)


class AbstractOrderAttachment(AbstractCommonField):
    class Angle(models.TextChoices):
        FRONT = 'front', _("Depan")
        SIDE = 'side', _("Samping")
        BACK = 'back', _("Belakang")

    order = models.ForeignKey('barber.Order', on_delete=models.CASCADE,
                              related_name='attachments')

    file = models.FileField(upload_to='order/%Y/%m/%d')
    filename = models.CharField(max_length=255, editable=False)
    filepath = models.CharField(max_length=255, editable=False)
    filesize = models.IntegerField(editable=False)
    filemime = models.CharField(max_length=255, editable=False)

    label = models.CharField(max_length=255, null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    angle = models.TextField(choices=Angle.choices, max_length=15)

    class Meta:
        abstract = True
        app_label = 'barber'
        ordering = ['-create_at']
        verbose_name = _("Order Attachment")
        verbose_name_plural = _("Order Attachments")

    def __str__(self) -> str:
        return self.label

    def save(self, *args, **kwargs):
        if not self.label:
            base = os.path.basename(self.file.name)
            self.label = base

        self.filesize = self.file.size
        super().save(*args, **kwargs)
