"""
Module to create custom buttons with round transparent white background.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    BooleanProperty,
    ObjectProperty
)

### Local imports ###

from tools.constants import (
    OPACITY_ON_BUTTON_PRESS
)
from tools import sound_mixer

#############
### Class ###
#############


class CircleIconButton(ButtonBehavior, Image):
    """
    A custom button with a white round rectangle background.
    """

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
