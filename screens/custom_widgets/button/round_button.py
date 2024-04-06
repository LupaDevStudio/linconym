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
    ColorProperty,
    BooleanProperty
)

### Local imports ###
from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    CONTENT_LABEL_FONT_SIZE,
    OPACITY_ON_BUTTON_PRESS
)

#############
### Class ###
#############


class RoundButton(ButtonBehavior, RelativeLayout):
    """
    A round button with a colored background and a label.
    """

    color = ColorProperty([1, 1, 1, 1])
    line_width = NumericProperty(1)
    text = StringProperty()
    text_filling_ratio = NumericProperty()
    font_size = NumericProperty()
    font_ratio = NumericProperty(1)
    disable_button = BooleanProperty(False)

    def __init__(
            self,
            text="",
            text_font_name=PATH_TEXT_FONT,
            text_filling_ratio=0.8,
            font_size=CONTENT_LABEL_FONT_SIZE,
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
        self.bind(disable_button=self.bind_function)
        self.bind(line_width=self.bind_function)

    def bind_function(self, base_widget, value):
        pass

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
