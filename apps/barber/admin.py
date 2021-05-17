from django.contrib import admin

from utils.generals import get_model

StyleCategory = get_model('barber', 'StyleCategory')
StyleItem = get_model('barber', 'StyleItem')
StyleAttachment = get_model('barber', 'StyleAttachment')
StyleOfTheYear = get_model('barber', 'StyleOfTheYear')
Booking = get_model('barber', 'Booking')
BookingAssigned = get_model('barber', 'BookingAssigned')
BookingRating = get_model('barber', 'BookingRating')
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


class BookingAssignedInline(admin.StackedInline):
    model = BookingAssigned


class BookingRatingInline(admin.StackedInline):
    model = BookingRating


class StyleItemExtend(admin.ModelAdmin):
    model = StyleItem
    inlines = [StyleAttachmentInline, ]


class BookingExtend(admin.ModelAdmin):
    model = Booking
    inlines = [BookingAssignedInline, BookingRatingInline, ]


class BranchExtend(admin.ModelAdmin):
    model = Branch
    inlines = [BranchBarbermanInline, BranchCashierInline, ]


admin.site.register(StyleCategory)
admin.site.register(StyleItem, StyleItemExtend)
admin.site.register(StyleOfTheYear)
admin.site.register(Booking, BookingExtend)
admin.site.register(Branch, BranchExtend)
admin.site.register(Brochure)
