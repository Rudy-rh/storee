from .general import *

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
