from django.contrib import admin

from utils.generals import get_model

StyleCategory = get_model('barber', 'StyleCategory')
StyleItem = get_model('barber', 'StyleItem')
StyleAttachment = get_model('barber', 'StyleAttachment')


class StyleAttachmentInline(admin.StackedInline):
    model = StyleAttachment


class StyleItemExtend(admin.ModelAdmin):
    model = StyleItem
    inlines = [StyleAttachmentInline, ]


admin.site.register(StyleCategory)
admin.site.register(StyleItem, StyleItemExtend)
