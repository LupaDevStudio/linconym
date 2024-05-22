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
    NumericProperty,
    BooleanProperty
)

#############
### Class ###
#############


class RewardFrame(RelativeLayout):
    """
    A layout displaying the amount of the reward and the image of the coin.
    """

    font_ratio = NumericProperty(1)
    reward = NumericProperty()
    radius = NumericProperty(12)
    unit = StringProperty("lincoin")
    plus_mode = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
