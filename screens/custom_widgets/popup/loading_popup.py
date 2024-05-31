"""
Module to create a popup to allow the user to regenerate lives.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.properties import (
    NumericProperty,
    StringProperty
)
from kivy.animation import Animation, AnimationTransition

### Local imports ###

from screens.custom_widgets.popup.custom_popup import CustomPopup


#############
### Class ###
#############


class LoadingPopup(CustomPopup):

    title = StringProperty()
    center_text = StringProperty()
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.center_text = "Loading in progress..."
        self.title = "Loading"

        anim1 = Animation(angle=360, duration=2,
                          t=AnimationTransition.linear)
        anim2 = Animation(angle=360, duration=2,
                          t=AnimationTransition.linear)
        self.sequence = anim1 + anim2
        self.sequence.repeat = True
        self.sequence.start(self)

    def on_dismiss(self):
        self.sequence.stop(self)
        return super().on_dismiss()

    def on_angle(self, item, angle):
        if angle >= 360:
            item.angle = angle - 360
