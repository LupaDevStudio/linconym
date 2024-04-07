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


class ActButton(ButtonBehavior, RelativeLayout):
    """
    A custom button with a white round rectangle background.
    """

    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    act_title = StringProperty()
    completion_text = StringProperty()
    font_size = NumericProperty(ACT_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)
    nb_levels = NumericProperty()
    nb_completed_levels = NumericProperty()
    nb_stars: Literal[0, 1, 2, 3] = NumericProperty()
    text_font_name = StringProperty(PATH_TEXT_FONT)
    primary_color = ColorProperty((1, 1, 1, 1))
    secondary_color = ColorProperty((0.5, 0.5, 0.5, 1))
    release_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.always_release = True
        self.bind(nb_completed_levels=self.update_nb_completed_levels)
        self.update_nb_completed_levels(None, None)

    def update_nb_completed_levels(self, base_widget, value):
        self.completion_text = str(
            self.nb_completed_levels) + "/" + str(self.nb_levels)

    def on_press(self):
        self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y):
            self.release_function()
        self.opacity = 1
