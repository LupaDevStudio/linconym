"""
Module to create coins counter.
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty,
    BooleanProperty
)

### Local imports ###
from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    OPACITY_ON_BUTTON_PRESS,
    EXPERIENCE_FONT_SIZE,
    THEMES_DICT
)

#############
### Class ###
#############


class ExperienceCounter(RelativeLayout):
    """
    A custom layout for the experience counter.
    """

    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    label_experience_left = StringProperty()
    percentage_experience = NumericProperty()
    experience_left = NumericProperty()
    font_size = NumericProperty(EXPERIENCE_FONT_SIZE)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    font_ratio = NumericProperty(1)
    theme_colors = StringProperty()
    primary_color = ColorProperty()
    secondary_color = ColorProperty()
    disable_button = BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(percentage_experience=self.update_experience)
        self.bind(experience_left=self.update_experience)
        self.bind(theme_colors=self.update_colors)

    def update_colors(self, base_widget, value):
        self.primary_color = THEMES_DICT[self.theme_colors]["primary"]
        self.secondary_color = THEMES_DICT[self.theme_colors]["secondary"]

    def update_experience(self, base_widget, value):
        self.label_experience_left = "+ " + str(self.experience_left) + " XP"

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            self.release_function()
            self.opacity = 1
