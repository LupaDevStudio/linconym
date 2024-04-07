"""
Module to create a popup with a custom style.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    ObjectProperty
)

### Local imports ###

from screens.custom_widgets.custom_popup import CustomPopup

#############
### Class ###
#############


class ImagePopup(CustomPopup):

    ok_button_label = StringProperty("Cancel")
    release_function = ObjectProperty(lambda: 1 + 1)
    image_source = StringProperty()
    mode = StringProperty()

    def __init__(self, **kwargs):
        if not "release_function" in kwargs:
            super().__init__(release_function=self.dismiss, **kwargs)
        else:
            super().__init__(**kwargs)
