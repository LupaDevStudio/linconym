"""
Module to create the money layout, with the amount and the unit icon.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_ICONS
)
from tools.constants import (
    COINS_COUNT_FONT_SIZE,
    get_lincoin_image_amount
)

#############
### Class ###
#############


class MoneyLayout(RelativeLayout):
    """
    A layout to display the money with the amount and the unit icon.
    """

    coins_count = NumericProperty(0)
    unit = StringProperty("lincoin")

    and_mode = BooleanProperty(False)
    or_mode = BooleanProperty(False)

    coins_count_text = StringProperty()
    coins_image_source = StringProperty(PATH_ICONS + "lincoin_1.png")

    font_size = NumericProperty(COINS_COUNT_FONT_SIZE)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    font_ratio = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.update_coins_count()
        self.bind(coins_count=self.update_coins_count)

    def update_coins_count(self, *args):
        self.coins_count_text = ""
        if self.and_mode:
            self.coins_count_text += "+ "
        elif self.or_mode:
            self.coins_count_text += " or "
        self.coins_count_text += str(self.coins_count)
        if self.unit == "lincoin":
            self.coins_image_source = get_lincoin_image_amount(self.coins_count)
        elif self.unit == "linclue":
            self.coins_image_source = PATH_ICONS + "linclue.png"
