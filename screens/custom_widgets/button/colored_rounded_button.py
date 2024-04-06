"""
Module to create custom buttons with round transparent white background.
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
    MAIN_BUTTON_FONT_SIZE,
)

#############
### Class ###
#############


class ColoredRoundedButton(ButtonBehavior, RelativeLayout):
    """
    A custom button with a colored round rectangle background.
    """

    background_color = ColorProperty()
    touch_color = ColorProperty()
    outline_color = ColorProperty()
    text = StringProperty()
    text_filling_ratio = NumericProperty()
    font_size = NumericProperty()
    font_ratio = NumericProperty(1)
    disable_button = BooleanProperty(False)
    color_label = ColorProperty()
    text_font_name = StringProperty(PATH_TEXT_FONT)

    def __init__(
            self,
            text="",
            text_font_name=PATH_TEXT_FONT,
            text_filling_ratio=0.8,
            font_size=MAIN_BUTTON_FONT_SIZE,
            release_function=lambda: 1 + 1,
            font_ratio=None,
            **kwargs):
        if font_ratio is not None:
            self.font_ratio = font_ratio
        super().__init__(**kwargs)
        self.release_function = release_function
        self.always_release = True
        self.text_font_name = text_font_name
        self.text = text
        self.text_filling_ratio = text_filling_ratio
        self.font_size = font_size

    def on_press(self):
        if not self.disable_button:
            self.temp_color = self.background_color
            self.background_color = self.touch_color

    def on_release(self):
        if not self.disable_button:
            self.background_color = self.temp_color
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
