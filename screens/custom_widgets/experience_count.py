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

    label_left = StringProperty()
    label_right = StringProperty()
    percentage_experience_before = NumericProperty()
    percentage_experience_won = NumericProperty()
    experience_displayed = NumericProperty()

    puzzle_mode = BooleanProperty(False)
    new_level = BooleanProperty(False)

    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    font_size = NumericProperty(EXPERIENCE_FONT_SIZE)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    font_ratio = NumericProperty(1)
    primary_color = ColorProperty()
    secondary_color = ColorProperty()
    radius = NumericProperty(15)
    ratio_foreground_progress_bar = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(experience_displayed=self.update_experience)
        self.bind(percentage_experience_before=self.update_experience)
        self.bind(percentage_experience_won=self.update_experience)
        self.bind(puzzle_mode=self.update_experience)
        self.bind(new_level=self.update_experience)

    def update_experience(self, base_widget, value):
        self.label_right = "+ " + str(self.experience_displayed) + " XP"
        if self.puzzle_mode:
            if not self.new_level:
                self.ratio_foreground_progress_bar = self.percentage_experience_before + self.percentage_experience_won
            else:
                self.ratio_foreground_progress_bar = self.percentage_experience_won
        else:
            self.ratio_foreground_progress_bar = 1
