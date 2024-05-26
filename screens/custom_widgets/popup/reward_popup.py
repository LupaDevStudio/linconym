"""
Module to create a popup to give a reward to the user.
"""

###############
### Imports ###
###############

### Python imports ###
from typing import Callable


### Kivy imports ###

from kivy.properties import (
    ObjectProperty,
    StringProperty,
    ColorProperty,
    NumericProperty,
    BooleanProperty
)

### Local imports ###

from screens.custom_widgets.popup.custom_popup import CustomPopup


#############
### Class ###
#############


class RewardPopup(CustomPopup):

    title = StringProperty("Reward")
    color_label_button = ColorProperty((1, 1, 1, 1))
    button_label = StringProperty("Close")
    top_label_text = StringProperty("You obtained:")
    release_function = ObjectProperty(lambda: 1 + 1)
    number_lincoins_won = NumericProperty(0)
    number_linclues_won = NumericProperty(0)

    def __init__(self, reward_function: Callable, **kwargs):
        def release_function():
            reward_function()
            self.dismiss()
        super().__init__(release_function=release_function, **kwargs)
