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
if not is_model_registered('barber', 'Booking'):
    class Booking(AbstractBooking):
        class Meta(AbstractBooking.Meta):
            db_table = 'barber_booking'

    __all__.append('Booking')


# 5
if not is_model_registered('barber', 'Branch'):
    class Branch(AbstractBranch):
        class Meta(AbstractBranch.Meta):
            db_table = 'barber_branch'

    __all__.append('Branch')


# 6
if not is_model_registered('barber', 'BranchBarberman'):
    class BranchBarberman(AbstractBranchBarberman):
        class Meta(AbstractBranchBarberman.Meta):
            db_table = 'barber_branch_barberman'

    __all__.append('BranchBarberman')


# 7
if not is_model_registered('barber', 'BranchCashier'):
    class BranchCashier(AbstractBranchCashier):
        class Meta(AbstractBranchCashier.Meta):
            db_table = 'barber_branch_cashier'

    __all__.append('BranchCashier')
