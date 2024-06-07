"""
Module to create the act button.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    ColorProperty,
    StringProperty,
    NumericProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    CONTENT_LABEL_FONT_SIZE
)

#############
### Class ###
#############


class BadgeLayout(RelativeLayout):
    """
    Layout for the badges, with image and title.
    """

    background_color = ColorProperty(CUSTOM_BUTTON_BACKGROUND_COLOR)
    title = StringProperty()
    image_source = StringProperty()
    font_size = NumericProperty(CONTENT_LABEL_FONT_SIZE)
    font_ratio = NumericProperty(1)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
