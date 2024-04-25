"""
Module to create a popup to allow the user to regenerate lives.
"""

###############
### Imports ###
###############


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


class LevelCompletedPopup(CustomPopup):

    title = StringProperty("Puzzle completed")
    color_label_button = ColorProperty((1, 1, 1, 1))
    right_button_label = StringProperty("Next puzzle")
    right_release_function = ObjectProperty(lambda: 1 + 1)
    left_button_label = StringProperty("Stay on puzzle")
    left_release_function = ObjectProperty(lambda: 1 + 1)
    top_label_text = StringProperty()
    nb_stars = NumericProperty()
    current_level_text = StringProperty()
    percentage_experience_before = NumericProperty()
    percentage_experience_won = NumericProperty()
    experience_displayed = NumericProperty()
    new_level = BooleanProperty(False)

    def __init__(self, **kwargs):
        if not "left_release_function" in kwargs:
            super().__init__(left_release_function=self.dismiss, **kwargs)
        else:
            super().__init__(**kwargs)
