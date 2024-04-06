"""
Module to a button with an image on the side.
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
    MAIN_BUTTON_FONT_SIZE,
)

#############
### Class ###
#############


class SideImageButton(ButtonBehavior, RelativeLayout):
    """
    A custom button with a white round rectangle background.
    """

    background_color = ColorProperty(CUSTOM_BUTTON_BACKGROUND_COLOR)
    text = StringProperty()
    coins_count = NumericProperty(-1)
    font_size = NumericProperty(MAIN_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)
    side_image_source = StringProperty()
    icon_mode = BooleanProperty(False)
    disable_button = BooleanProperty(False)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    def __init__(
            self,
            release_function=lambda: 1 + 1,
            **kwargs):
        super().__init__(**kwargs)
        self.release_function = release_function
        self.always_release = True

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
