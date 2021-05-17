from .general import *
from .booking import *
from .branch import *

from utils.generals import is_model_registered

__all__ = list()


# 1
if not is_model_registered('barber', 'StyleCategory'):
    class StyleCategory(AbstractStyleCategory):
        class Meta(AbstractStyleCategory.Meta):
            db_table = 'barber_style_category'

    __all__.append('StyleCategory')


# 2
if not is_model_registered('barber', 'StyleItem'):
    class StyleItem(AbstractStyleItem):
        class Meta(AbstractStyleItem.Meta):
            db_table = 'barber_style_item'

    __all__.append('StyleItem')


# 3
if not is_model_registered('barber', 'StyleAttachment'):
    class StyleAttachment(AbstractStyleAttachment):
        class Meta(AbstractStyleAttachment.Meta):
            db_table = 'barber_style_attachment'

    __all__.append('StyleAttachment')


# 4
if not is_model_registered('barber', 'StyleOfTheYear'):
    class StyleOfTheYear(AbstractStyleOfTheYear):
        class Meta(AbstractStyleOfTheYear.Meta):
            db_table = 'barber_style_oty'

    __all__.append('StyleOfTheYear')


# 5
if not is_model_registered('barber', 'Booking'):
    class Booking(AbstractBooking):
        class Meta(AbstractBooking.Meta):
            db_table = 'barber_booking'

    __all__.append('Booking')


# 6
if not is_model_registered('barber', 'Branch'):
    class Branch(AbstractBranch):
        class Meta(AbstractBranch.Meta):
            db_table = 'barber_branch'

    __all__.append('Branch')


# 7
if not is_model_registered('barber', 'BranchBarberman'):
    class BranchBarberman(AbstractBranchBarberman):
        class Meta(AbstractBranchBarberman.Meta):
            db_table = 'barber_branch_barberman'

    __all__.append('BranchBarberman')


# 8
if not is_model_registered('barber', 'BranchCashier'):
    class BranchCashier(AbstractBranchCashier):
        class Meta(AbstractBranchCashier.Meta):
            db_table = 'barber_branch_cashier'

    __all__.append('BranchCashier')


# 9
if not is_model_registered('barber', 'Brochure'):
    class Brochure(AbstractBrochure):
        class Meta(AbstractBrochure.Meta):
            db_table = 'barber_brochure'

    __all__.append('Brochure')


# 10
if not is_model_registered('barber', 'BookingAssigned'):
    class BookingAssigned(AbstractBookingAssigned):
        class Meta(AbstractBookingAssigned.Meta):
            db_table = 'barber_booking_assigned'

    __all__.append('BookingAssigned')


# 11
if not is_model_registered('barber', 'BookingRating'):
    class BookingRating(AbstractBookingRating):
        class Meta(AbstractBookingRating.Meta):
            db_table = 'barber_booking_rating'

    __all__.append('BookingRating')
