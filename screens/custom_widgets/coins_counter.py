"""
Module to create coins counter.
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ObjectProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_ICONS
)
from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    OPACITY_ON_BUTTON_PRESS,
    COINS_COUNT_FONT_SIZE
)

#############
### Class ###
#############


class CoinsCounter(ButtonBehavior, RelativeLayout):
    """
    A custom button with a white round rectangle background.
    """

    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    coins_count = NumericProperty(0)
    unit = StringProperty("lincoin")
    font_size = NumericProperty(COINS_COUNT_FONT_SIZE)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    font_ratio = NumericProperty(1)
    display_plus = BooleanProperty(True)
    disable_button = BooleanProperty(False)
    radius = NumericProperty(15)
    release_function = ObjectProperty(lambda: 1 + 1)
    coins_image_source = StringProperty(PATH_ICONS + "lincoin_1.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.always_release = True

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            self.release_function()
            self.opacity = 1
