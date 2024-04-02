"""
Module to create custom buttons with round transparent white background.
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.uix.widget import Widget
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
    MAIN_BUTTON_FONT_SIZE,
    OPACITY_ON_BUTTON_PRESS
)

#############
### Class ###
#############


class CustomButton(ButtonBehavior, Widget):
    """
    A custom button with a white round rectangle background.
    """

    background_color = ColorProperty(CUSTOM_BUTTON_BACKGROUND_COLOR)
    text = StringProperty()
    text_font_name = StringProperty(PATH_TEXT_FONT)
    text_filling_ratio = NumericProperty(0.8)
    font_size = NumericProperty(MAIN_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)
    radius = NumericProperty(25)
    disable_button = BooleanProperty(False)
    release_function = ObjectProperty()

    def __init__(
            self,
            font_ratio=None,
            **kwargs):
        if font_ratio is not None:
            self.font_ratio = font_ratio
        super().__init__(**kwargs)
        self.always_release = True

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            self.opacity = 1
            self.release_function()
