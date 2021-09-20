from django.contrib import admin

from utils.generals import get_model

StyleCategory = get_model('barber', 'StyleCategory')
StyleItem = get_model('barber', 'StyleItem')
StyleAttachment = get_model('barber', 'StyleAttachment')
StyleOfTheYear = get_model('barber', 'StyleOfTheYear')
Order = get_model('barber', 'Order')
OrderAssigned = get_model('barber', 'OrderAssigned')
OrderRating = get_model('barber', 'OrderRating')
OrderAttachment = get_model('barber', 'OrderAttachment')
Branch = get_model('barber', 'Branch')
BranchBarberman = get_model('barber', 'BranchBarberman')
BranchCashier = get_model('barber', 'BranchCashier')
Brochure = get_model('barber', 'Brochure')
Rules = get_model('barber', 'Rules')
WorkStandardCategory = get_model('barber', 'WorkStandardCategory')
WorkStandardSection = get_model('barber', 'WorkStandardSection')
Banner = get_model('barber', 'Banner')
Information = get_model('barber', 'Information')
InformationRead = get_model('barber', 'InformationRead')


class StyleAttachmentInline(admin.StackedInline):
    model = StyleAttachment
    readonly_fields = ['image_preview', ]

    def image_preview(self, instance):
        from django.utils.html import escape
        from django.utils.safestring import mark_safe

        x = '08972526262'
        y = x.replace('0', '62', 1)
        print(y)

        if x.startswith('0'):
            print('AAAAA')

        return mark_safe('<img src="%s" width="120" />' %
                         escape(instance.image.url))
    image_preview.allow_tags = True


class BranchBarbermanInline(admin.StackedInline):
    model = BranchBarberman


class BranchCashierInline(admin.StackedInline):
    model = BranchCashier


class OrderAssignedInline(admin.StackedInline):
    model = OrderAssigned


class OrderRatingInline(admin.StackedInline):
    model = OrderRating


class OrderAttachmentInline(admin.StackedInline):
    model = OrderAttachment


class StyleItemExtend(admin.ModelAdmin):
    model = StyleItem
    inlines = [StyleAttachmentInline, ]
    list_display = ['label', 'image_preview', ]

    def image_preview(self, instance):
        from django.utils.html import escape
        from django.utils.safestring import mark_safe

        images = []
        attachments = instance.attachments.all()
        for attach in attachments:
            image = mark_safe('<img src="%s" width="100" />' %
                              escape(attach.image.url))
            images.append(image)
        return mark_safe(''.join(images))
    image_preview.short_description = "Image"
    image_preview.allow_tags = True


class OrderExtend(admin.ModelAdmin):
    model = Order
    inlines = [OrderAssignedInline, OrderRatingInline, OrderAttachmentInline, ]


class BranchExtend(admin.ModelAdmin):
    model = Branch
    inlines = [BranchBarbermanInline, BranchCashierInline, ]


class WorkStandardSectionExtend(admin.ModelAdmin):
    model = WorkStandardSection
    list_filter = ['category', ]
    list_display = ['label', 'category', ]


admin.site.register(StyleCategory)
admin.site.register(StyleItem, StyleItemExtend)
admin.site.register(StyleOfTheYear)
admin.site.register(Order, OrderExtend)
admin.site.register(Branch, BranchExtend)
admin.site.register(Brochure)
admin.site.register(Rules)
admin.site.register(WorkStandardCategory)
admin.site.register(WorkStandardSection, WorkStandardSectionExtend)
admin.site.register(Banner)
admin.site.register(Information)
admin.site.register(InformationRead)
