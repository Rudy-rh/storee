from django.db import models
from .abstract import AbstractCommonField


class AbstractStyleCategory(AbstractCommonField):
    label = models.CharField(max_length=255)

    class Meta:
        abstract = True
        app_label = 'barber'

    def __str__(self) -> str:
        return self.label


class AbstractStyleItem(AbstractCommonField):
    style_category = models.OneToOneField('barber.StyleCategory', on_delete=models.CASCADE,
                                          related_name='items')

    label = models.CharField(max_length=255, null=True, blank=True,
                             editable=False)

    class Meta:
        abstract = True
        app_label = 'barber'

    def __str__(self) -> str:
        return self.label or self.style_category.label

    def save(self, *args, **kwargs):
        self.label = self.style_category.label
        super().save(*args, **kwargs)


class AbstractStyleAttachment(AbstractCommonField):
    style_item = models.ForeignKey('barber.StyleItem', on_delete=models.CASCADE,
                                   related_name='attachments')

    label = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='style/attachment')

    class Meta:
        abstract = True
        app_label = 'barber'

    def __str__(self) -> str:
        return self.label or self.image.name
