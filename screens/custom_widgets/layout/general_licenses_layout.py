"""
Module to create the act button.
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
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    LABEL_FONT_SIZE,
    OPACITY_ON_BUTTON_PRESS
)

#############
### Class ###
#############


class GeneralLicensesLayout(ButtonBehavior, RelativeLayout):
    """
    The general license layout with a white round rectangle background.
    It is composed of a title, and it links to the credits url.
    """

    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    license_title = StringProperty()
    font_size = NumericProperty(LABEL_FONT_SIZE)
    font_ratio = NumericProperty(1)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    primary_color = ColorProperty((1, 1, 1, 1))
    radius = NumericProperty(40)
    release_function = ObjectProperty()
    disable_button = BooleanProperty(False)

    def __init__(
            self,
            release_function=lambda: 1 + 1,
            font_ratio=None,
            **kwargs):

        if font_ratio is not None:
            self.font_ratio = font_ratio

        self.release_function = release_function
        self.always_release = True

        super().__init__(**kwargs)

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
