"""
Module to create custom progress bar.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.widget import (
    Widget
)
from kivy.properties import (
    ColorProperty,
    NumericProperty
)

#############
### Class ###
#############


class CustomProgressBar(Widget):
    """
    A custom button with a white round rectangle background.
    """

    primary_color = ColorProperty()
    secondary_color = ColorProperty()
    value = NumericProperty(0.5)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
