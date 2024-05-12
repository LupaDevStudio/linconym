"""
Module to create buy and enable buttons
"""


###############
### Imports ###
###############

### Python imports ###

from typing import Literal

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ObjectProperty,
    ColorProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    OPACITY_ON_BUTTON_PRESS,
    ACT_BUTTON_FONT_SIZE,
    SMALL_BUYING_BUTTON_FONT_SIZE
)

#############
### Class ###
#############


class BuyButton(ButtonBehavior, RelativeLayout):
    """
    A button for the customization screen to buy images or colors.
    """

    background_color = ColorProperty(CUSTOM_BUTTON_BACKGROUND_COLOR)
    button_title = StringProperty()
    font_size = NumericProperty(SMALL_BUYING_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    has_bought = BooleanProperty(False)
    is_using = BooleanProperty(False)
    price = NumericProperty(0)
    price_text = StringProperty("0")
    release_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.always_release = True

        # Bind the price to update the value in real time
        self.bind(price=self.update_price)

    def update_price(self, base_widget, value):
        self.price_text = str(self.price)

    def update_display(self):
        if self.has_bought:
            self.ids["price_label"].opacity = 0
            self.ids["coins_image"].opacity = 0
            self.ids["selection_circle"].opacity = 1
        else:
            self.ids["price_label"].opacity = 1
            self.ids["coins_image"].opacity = 1
            self.ids["selection_circle"].opacity = 0
        if self.is_using:
            self.ids["activated_image"].opacity = 1
        else:
            self.ids["activated_image"].opacity = 0

    def on_press(self):
        self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y):
            self.release_function()
        self.opacity = 1
