from .general import *
from .order import *
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
if not is_model_registered('barber', 'Order'):
    class Order(AbstractOrder):
        class Meta(AbstractOrder.Meta):
            db_table = 'barber_order'

    __all__.append('Order')


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
if not is_model_registered('barber', 'OrderAssigned'):
    class OrderAssigned(AbstractOrderAssigned):
        class Meta(AbstractOrderAssigned.Meta):
            db_table = 'barber_order_assigned'

    __all__.append('OrderAssigned')


# 11
if not is_model_registered('barber', 'OrderRating'):
    class OrderRating(AbstractOrderRating):
        class Meta(AbstractOrderRating.Meta):
            db_table = 'barber_order_rating'

    __all__.append('OrderRating')


# 12
if not is_model_registered('barber', 'Rules'):
    class Rules(AbstractRules):
        class Meta(AbstractRules.Meta):
            db_table = 'barber_rules'

    __all__.append('Rules')
