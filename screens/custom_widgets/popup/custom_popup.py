"""
Module to create a popup with a custom style.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.popup import Popup
from kivy.properties import (
    ColorProperty,
    NumericProperty,
    ObjectProperty
)

#############
### Class ###
#############


class CustomPopup(Popup):

    primary_color = ColorProperty((0.3, 0.3, 0.3, 1))
    secondary_color = ColorProperty((0.3, 0.3, 0.3, 1))
    font_ratio = NumericProperty(1)
    size_hint = ObjectProperty((0.85, 0.6))
