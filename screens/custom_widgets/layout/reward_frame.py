"""
Module to create buy and enable buttons
"""


###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    NumericProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_ICONS
)
from tools.constants import (
    ACT_BUTTON_FONT_SIZE
)

#############
### Class ###
#############


class RewardFrame(RelativeLayout):
    """
    A layout displaying the amount of the reward and the image of the coin.
    """

    font_size = NumericProperty(ACT_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    text = StringProperty()
    radius = NumericProperty(12)
    image_source = StringProperty(PATH_ICONS + "lincoin_1.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
