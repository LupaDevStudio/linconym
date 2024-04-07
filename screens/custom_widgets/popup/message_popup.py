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


class MessagePopup(CustomPopup):

    ok_button_label = StringProperty("Cancel")
    center_label_text = StringProperty()
    release_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        if not "release_function" in kwargs:
            super().__init__(release_function=self.dismiss, **kwargs)
        else:
            super().__init__(**kwargs)
