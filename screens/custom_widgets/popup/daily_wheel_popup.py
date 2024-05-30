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
    NumericProperty
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Daily Wheel"
        number_of_turns = rd.randint(4, 8)
        last_angle = rd.randint(0, 360) + 360 * number_of_turns
        anim = Animation(angle=last_angle, duration=number_of_turns+1,
                         t=AnimationTransition.out_quad)
        anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0
