"""
Module to create buy and enable buttons
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
    ColorProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    OPACITY_ON_BUTTON_PRESS,
    ACT_BUTTON_FONT_SIZE
)

#############
### Class ###
#############


class BuyRectangleButton(ButtonBehavior, RelativeLayout):
    """
    A button for the customization screen to buy images or colors.
    """

    font_size = NumericProperty()
    font_ratio = NumericProperty(1)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    price = NumericProperty()
    price_text = StringProperty()
    disable_button = BooleanProperty(False)
    background_color = ColorProperty(CUSTOM_BUTTON_BACKGROUND_COLOR)
    mode = StringProperty("line")
    radius = NumericProperty(12)

    def __init__(
            self,
            button_title: str = None,
            text_font_name=PATH_TEXT_FONT,
            font_size=ACT_BUTTON_FONT_SIZE,
            has_bought: bool = False,
            is_using: bool = False,
            price: int = 0,
            release_function=lambda: 1 + 1,
            font_ratio=None,
            **kwargs):

        if button_title is not None:
            self.button_title = button_title
        if font_ratio is not None:
            self.font_ratio = font_ratio

        self.release_function = release_function
        self.has_bought = has_bought
        self.is_using = is_using
        self.price = price
        self.price_text = str(self.price)
        self.always_release = True

        super().__init__(**kwargs)
        self.text_font_name = text_font_name
        self.font_size = font_size

        # Bind the price to update the value in real time
        self.bind(price=self.update_price)

    def update_price(self, base_widget, value):
        self.price_text = str(self.price)

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            self.release_function()
            self.opacity = 1
