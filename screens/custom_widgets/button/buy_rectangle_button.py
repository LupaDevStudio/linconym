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
    ColorProperty,
    ObjectProperty
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

    font_size = NumericProperty(ACT_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    price = NumericProperty(0)
    price_text = StringProperty("0")
    disable_button = BooleanProperty(False)
    background_color = ColorProperty(CUSTOM_BUTTON_BACKGROUND_COLOR)
    mode = StringProperty("line")
    radius = NumericProperty(12)
    button_title = StringProperty()
    release_function = ObjectProperty(lambda: 1 + 1)
    has_bought = BooleanProperty(False)
    is_using = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.always_release = True

        # Bind the price to update the value in real time
        self.bind(price=self.update_price)

    def update_price(self, base_widget, value):
        self.price_text = str(self.price)

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
