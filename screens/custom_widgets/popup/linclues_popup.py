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

#############
### Class ###
#############


class LincluesPopup(CustomPopup):

    title = StringProperty("Clues")
    color_label_button = ColorProperty((1, 1, 1, 1))
    right_button_label = StringProperty("Yes")
    right_release_function = ObjectProperty(lambda: 1 + 1)
    left_button_label = StringProperty("No")
    left_release_function = ObjectProperty(lambda: 1 + 1)
    text = StringProperty()
    number_linclues = NumericProperty(0)
    number_linclues_to_use = NumericProperty(0)
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

        self.bind(number_linclues_to_use=self.update_popup)
        self.bind(number_linclues=self.update_popup)
        self.update_popup()

    def update_popup(self, *args):
        self.text = f"Do you want to use {self.number_linclues_to_use} Linclues to have a clue on the current puzzle?\n\nThe clue word will be given from the current position in the tree."
        # Mark the singular
        if self.number_linclues_to_use == 1:
            self.text = self.text.replace("Linclues", "Linclue")
        
        if self.number_linclues_to_use > self.number_linclues:
            self.ids.right_button.disabled = True
        else:
            if self.game.current_word != self.game.end_word:
                self.ids.right_button.disabled = False
            else:
                self.ids.right_button.disabled = True
