"""
Module to create a popup to allow the user to regenerate lives.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty,
    ObjectProperty
)
from kivy.animation import Animation, AnimationTransition

### Local imports ###

from screens.custom_widgets.popup.custom_popup import CustomPopup


#############
### Class ###
#############


class DailyWheelPopup(CustomPopup):

    title = StringProperty()
    angle = NumericProperty(0)
    primary_color = ColorProperty()
    secondary_color = ColorProperty()
    color_label_button = ColorProperty((1, 1, 1, 1))
    release_function = ObjectProperty(lambda: 1 + 1)
    button_label = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Daily Wheel"

    def on_open(self):
        self.release_function = self.start_animation
        self.button_label = "Spin"
        return super().on_open()

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0

    def start_animation(self):
        number_of_turns = rd.randint(4, 7)
        last_angle = rd.randint(0, 360) + 360 * number_of_turns
        anim = Animation(angle=last_angle, duration=number_of_turns,
                         t=AnimationTransition.out_quad)
        anim.start(self)
        self.ids.button.disabled = True
        anim.on_complete = self.finish_animation

    def finish_animation(self, *args):
        self.button_label = "Close"
        self.ids.button.disabled = False
        self.release_function = self.dismiss
