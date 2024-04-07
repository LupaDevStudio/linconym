"""
Module to create a popup to allow the user to regenerate lives.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.properties import (
    ObjectProperty,
    StringProperty
)

### Local imports ###

from screens.custom_widgets.popup.custom_popup import CustomPopup


#############
### Class ###
#############


class TwoButtonsPopup(CustomPopup):

    title = StringProperty()
    right_button_label = StringProperty()
    right_release_function = ObjectProperty(lambda: 1 + 1)
    left_button_label = StringProperty("Cancel")
    left_release_function = ObjectProperty(lambda: 1 + 1)
    center_label_text = StringProperty()

    def __init__(self, **kwargs):
        if not "left_release_function" in kwargs:
            super().__init__(left_release_function=self.dismiss, **kwargs)
        else:
            super().__init__(**kwargs)
