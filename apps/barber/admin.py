from django.contrib import admin

from utils.generals import get_model

StyleCategory = get_model('barber', 'StyleCategory')
StyleItem = get_model('barber', 'StyleItem')
StyleAttachment = get_model('barber', 'StyleAttachment')
StyleOfTheYear = get_model('barber', 'StyleOfTheYear')
Booking = get_model('barber', 'Booking')
Branch = get_model('barber', 'Branch')
BranchBarberman = get_model('barber', 'BranchBarberman')
BranchCashier = get_model('barber', 'BranchCashier')
Brochure = get_model('barber', 'Brochure')


class StyleAttachmentInline(admin.StackedInline):
    model = StyleAttachment


class BranchBarbermanInline(admin.StackedInline):
    model = BranchBarberman


class BranchCashierInline(admin.StackedInline):
    model = BranchCashier


class StyleItemExtend(admin.ModelAdmin):
    model = StyleItem
    inlines = [StyleAttachmentInline, ]


class BranchExtend(admin.ModelAdmin):
    model = Branch
    inlines = [BranchBarbermanInline, BranchCashierInline, ]


admin.site.register(StyleCategory)
admin.site.register(StyleItem, StyleItemExtend)
admin.site.register(StyleOfTheYear)
admin.site.register(Booking)
admin.site.register(Branch, BranchExtend)
admin.site.register(Brochure)
