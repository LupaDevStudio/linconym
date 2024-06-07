"""
Module to create custom buttons with round transparent white background.
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ObjectProperty
)

### Local imports ###
from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    OPACITY_ON_BUTTON_PRESS,
    CONTENT_LABEL_FONT_SIZE,
    LABEL_FONT_SIZE
)
from tools import sound_mixer

#############
### Class ###
#############


class CustomContentButton(ButtonBehavior, RelativeLayout):
    """
    A custom button with a white round rectangle background.
    """

    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    title = StringProperty()
    content = StringProperty()
    text_filling_ratio = NumericProperty(0.875)
    font_size_title = NumericProperty(LABEL_FONT_SIZE)
    font_size_content = NumericProperty(CONTENT_LABEL_FONT_SIZE)
    font_ratio = NumericProperty(1)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    disable_button = BooleanProperty(False)
    release_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.always_release = True

    def on_press(self):
        if not self.disable_button:
            sound_mixer.play("button_click")
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
