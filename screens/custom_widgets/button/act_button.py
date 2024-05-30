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
    ObjectProperty,
    BooleanProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    OPACITY_ON_BUTTON_PRESS,
    ACT_BUTTON_FONT_SIZE
)
from tools import sound_mixer

#############
### Class ###
#############


class ActButton(ButtonBehavior, RelativeLayout):
    """
    A custom button with a white round rectangle background.
    """

    act_title = StringProperty()
    completion_text = StringProperty()
    unlock_text = StringProperty()
    font_size = NumericProperty(ACT_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)
    nb_levels = NumericProperty()
    nb_completed_levels = NumericProperty()
    nb_stars_to_unlock = NumericProperty()
    nb_total_stars = NumericProperty()
    nb_stars: Literal[0, 1, 2, 3] = NumericProperty()
    text_font_name = StringProperty(PATH_TEXT_FONT)
    primary_color = ColorProperty((1, 1, 1, 1))
    secondary_color = ColorProperty((0.5, 0.5, 0.5, 1))
    release_function = ObjectProperty(lambda: 1 + 1)
    disable_button = BooleanProperty(False)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.always_release = True
        self.bind(nb_completed_levels=self.update_nb_completed_levels)
        self.bind(nb_total_stars=self.update_unlock_stars)
        self.update_nb_completed_levels()
        self.update_unlock_stars()

    def update_nb_completed_levels(self, base_widget=None, value=None):
        self.completion_text = f"{self.nb_completed_levels}/{self.nb_levels} levels"

    def update_unlock_stars(self, base_widget=None, value=None):
        self.unlock_text = str(
            self.nb_total_stars) + "/" + str(self.nb_stars_to_unlock)

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS
            sound_mixer.play("button_click")

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y) and not self.disable_button:
            self.release_function()
        self.opacity = 1
