import os

from django.db import models
from django.contrib.auth.models import Group

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


class AbstractStyleOfTheYear(AbstractCommonField):
    label = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='style/soty')

    class Meta:
        abstract = True
        app_label = 'barber'
        ordering = ['-create_at']

    def __str__(self) -> str:
        return self.label or self.image.name

    def save(self, *args, **kwargs):
        if not self.label:
            base = os.path.basename(self.image.name)
            self.label = base
        super().save(*args, **kwargs)


class AbstractBrochure(AbstractCommonField):
    label = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='brochure')
    position = models.IntegerField(default=1)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'barber'
        ordering = ['-create_at']

    def __str__(self) -> str:
        return self.label or self.image.name

    def save(self, *args, **kwargs):
        if not self.label:
            base = os.path.basename(self.image.name)
            self.label = base
        super().save(*args, **kwargs)


class AbstractRules(AbstractCommonField):
    label = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='brochure')
    position = models.IntegerField(default=1)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'barber'
        ordering = ['-create_at']

    def __str__(self) -> str:
        return self.label or self.image.name

    def save(self, *args, **kwargs):
        if not self.label:
            base = os.path.basename(self.image.name)
            self.label = base
        super().save(*args, **kwargs)


class AbstractWorkStandardCategory(AbstractCommonField):
    groups = models.ForeignKey(Group, on_delete=models.CASCADE,
                               related_name='standard_categories')
    label = models.CharField(max_length=255)

    class Meta:
        abstract = True
        app_label = 'barber'
        ordering = ['-create_at']

    def __str__(self) -> str:
        return '[{}] {}'.format(self.groups.name, self.label)


class AbstractWorkStandardSection(AbstractCommonField):
    category = models.ForeignKey('barber.WorkStandardCategory',
                                 on_delete=models.CASCADE,
                                 related_name='standard_sections')

    label = models.CharField(max_length=255)
    video_url = models.URLField(max_length=255, null=True, blank=True)
    video_file = models.FileField(max_length=500, upload_to='video',
                                  null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'barber'
        ordering = ['-create_at']

    def __str__(self) -> str:
        return self.label
