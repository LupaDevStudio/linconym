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
    ColorProperty,
    ObjectProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from tools import sound_mixer

#############
### Class ###
#############


class ColoredRoundedButtonImage(ButtonBehavior, RelativeLayout):
    """
    A custom button with a colored round rectangle background and an image in it.
    """

    background_color = ColorProperty()
    touch_color = ColorProperty()
    image_path = StringProperty()
    text_filling_ratio = NumericProperty()
    font_size = NumericProperty()
    font_ratio = NumericProperty(1)
    disable_button = BooleanProperty(False)
    color_image = ColorProperty()
    text_font_name = StringProperty(PATH_TEXT_FONT)
    release_function = ObjectProperty(lambda: 1 + 1)
    use_default_sound = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.always_release = True

    def on_press(self):
        if not self.disable_button:
            self.temp_color = self.background_color
            self.background_color = self.touch_color
            if self.use_default_sound:
                sound_mixer.play("button_click")

    def on_release(self):
        if not self.disable_button:
            self.background_color = self.temp_color
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
