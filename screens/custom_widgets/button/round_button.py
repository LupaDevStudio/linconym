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
    BooleanProperty,
    ObjectProperty
)

### Local imports ###
from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    CONTENT_LABEL_FONT_SIZE,
    OPACITY_ON_BUTTON_PRESS,
    DICT_CONVERSION_MONEY
)
from tools import sound_mixer

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
    text_filling_ratio = NumericProperty(0.8)
    font_size = NumericProperty(CONTENT_LABEL_FONT_SIZE)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    font_ratio = NumericProperty(1)
    disable_button = BooleanProperty(False)
    release_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.always_release = True

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS
            sound_mixer.play("button_click")

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
