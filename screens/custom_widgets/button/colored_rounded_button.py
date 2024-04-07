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
    ColorProperty,
    ObjectProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    MAIN_BUTTON_FONT_SIZE,
    OUTLINE_RECTANGLE_COLORED_ROUNDED_BUTTON
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
    text_filling_ratio = NumericProperty(0.8)
    font_size = NumericProperty(MAIN_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)
    disable_button = BooleanProperty(False)
    color_label = ColorProperty()
    text_font_name = StringProperty(PATH_TEXT_FONT)
    release_function = ObjectProperty()
    outline_width = NumericProperty(OUTLINE_RECTANGLE_COLORED_ROUNDED_BUTTON/2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.always_release = True

    def on_press(self):
        if not self.disable_button:
            self.temp_color = self.background_color
            self.background_color = self.touch_color

    def on_release(self):
        if not self.disable_button:
            self.background_color = self.temp_color
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
