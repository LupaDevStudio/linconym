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
    NumericProperty
)

### Local imports ###

from screens.custom_widgets.popup.custom_popup import CustomPopup
from tools.constants import (
    DICT_CONVERSION_MONEY
)

#############
### Class ###
#############


class ConversionPopup(CustomPopup):

    title = StringProperty("Clues")
    color_label_button = ColorProperty((1, 1, 1, 1))
    right_button_label = StringProperty("Yes")
    right_release_function = ObjectProperty(lambda: 1 + 1)
    left_button_label = StringProperty("No")
    left_release_function = ObjectProperty(lambda: 1 + 1)
    text = StringProperty()
    number_linclues = NumericProperty(DICT_CONVERSION_MONEY["reward_linclues"])
    number_lincoins = NumericProperty(DICT_CONVERSION_MONEY["price_lincoins"])
    game = ObjectProperty()

    def __init__(self, yes_function: Callable = lambda: 1 + 1, **kwargs):

        # Define right function
        def right_release_function():
            yes_function()
            self.dismiss()

        if not "left_release_function" in kwargs:
            super().__init__(left_release_function=self.dismiss,
                             right_release_function=right_release_function, **kwargs)
        else:
            super().__init__(right_release_function=right_release_function, **kwargs)

        self.update_popup()

    def update_popup(self, *args):
        self.text = f"Do you want to convert {self.number_lincoins} Lincoins to get {self.number_linclues} Linclue?"
