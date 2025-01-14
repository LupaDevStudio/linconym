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
    PATH_TITLE_FONT
)
from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    OPACITY_ON_BUTTON_PRESS
)

#############
### Class ###
#############


class SelectCircleButtonWithText(ButtonBehavior, RelativeLayout):
    """
    A button for the customization screen to buy images or colors.
    """

    background_color = ColorProperty(CUSTOM_BUTTON_BACKGROUND_COLOR)
    font_ratio = NumericProperty(1)
    text_filling_ratio = NumericProperty(0.6)
    font_size = NumericProperty()
    is_using = BooleanProperty(False)
    disable_button = BooleanProperty(False)
    text = StringProperty()
    text_font_name = StringProperty(PATH_TITLE_FONT)
    radius = NumericProperty(25)
    release_function = ObjectProperty(lambda: 1 + 1)

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
