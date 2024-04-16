"""
Module to create the act button.
"""

###############
### Imports ###
###############

### Python imports ###

from typing import Literal

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    StringProperty,
    NumericProperty,
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


class ActButton(ButtonBehavior, RelativeLayout):
    """
    A custom button with a white round rectangle background.
    """

    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    act_title = StringProperty()
    completion_text = StringProperty()
    unlock_text = StringProperty()
    font_size = NumericProperty()
    font_ratio = NumericProperty()
    nb_levels = NumericProperty()
    nb_completed_levels = NumericProperty()
    nb_stars = NumericProperty()
    nb_stars_to_unlock = NumericProperty()
    nb_total_stars = NumericProperty()
    text_font_name = StringProperty(PATH_TEXT_FONT)
    primary_color = ColorProperty((1, 1, 1, 1))
    secondary_color = ColorProperty((0.5, 0.5, 0.5, 1))

    def __init__(
            self,
            text_font_name=PATH_TEXT_FONT,
            font_size=ACT_BUTTON_FONT_SIZE,
            release_function=lambda: 1 + 1,
            **kwargs):

        super().__init__(**kwargs)
        self.release_function = release_function
        self.always_release = True
        self.text_font_name = text_font_name
        self.font_size = font_size
        self.bind(nb_completed_levels=self.update_nb_completed_levels)
        self.bind(nb_total_stars=self.update_unlock_stars)
        self.update_nb_completed_levels()
        self.update_unlock_stars()

    def update_nb_completed_levels(self, base_widget=None, value=None):
        self.completion_text = str(
            self.nb_completed_levels) + "/" + str(self.nb_levels)

    def update_unlock_stars(self, base_widget=None, value=None):
        self.unlock_text = str(
            self.nb_total_stars) + "/" + str(self.nb_stars_to_unlock)

    def on_press(self):
        self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y):
            self.release_function()
        self.opacity = 1
