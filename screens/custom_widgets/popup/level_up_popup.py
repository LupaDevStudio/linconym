"""
Module to create a popup to allow the user to regenerate lives.
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
from tools import sound_mixer


#############
### Class ###
#############


class LevelUpPopup(CustomPopup):

    title = StringProperty("Level up")
    color_label_button = ColorProperty((1, 1, 1, 1))
    button_label = StringProperty("Close")
    top_label_text = StringProperty("Congratulations, you levelled up!")
    release_function = ObjectProperty(lambda: 1 + 1)
    number_lincoins_won = NumericProperty(0)
    has_changed_status = BooleanProperty(False)
    current_status = StringProperty()
    next_status = StringProperty()

    def __init__(self, **kwargs):
        if not "release_function" in kwargs:
            super().__init__(release_function=self.dismiss, **kwargs)
        else:
            super().__init__(**kwargs)

    def open(self, *_args, **kwargs):
        sound_mixer.play("level_up")
        return super().open(*_args, **kwargs)
