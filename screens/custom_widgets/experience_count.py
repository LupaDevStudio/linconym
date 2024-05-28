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
    EXPERIENCE_FONT_SIZE,
    USER_DATA
)
from tools.levels import (
    compute_xp_to_level_up
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
    progress = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_experience(None, None)
        self.bind(experience_displayed=self.update_experience)
        self.bind(percentage_experience_before=self.update_experience)
        self.bind(percentage_experience_won=self.update_experience)
        self.bind(puzzle_mode=self.update_experience)
        self.bind(new_level=self.update_experience)

    def update_experience(self, base_widget, value):
        if self.puzzle_mode:
            if self.experience_displayed == 0:
                self.label_right = ""
            else:
                self.label_right = "+ " + str(self.experience_displayed) + " XP"
            
            if not self.new_level:
                if self.percentage_experience_before == 0 and self.percentage_experience_won == 0:
                    self.progress = 0
                else:
                    self.progress = 1 - self.percentage_experience_won / \
                        (self.percentage_experience_won +
                         self.percentage_experience_before)

            else:
                self.progress = 1
        else:
            total_experience = compute_xp_to_level_up(USER_DATA.user_profile["level"])
            current_experience = int(total_experience * self.percentage_experience_before)
            self.label_right = str(current_experience) + " / " + str(total_experience)
            self.progress = 1
        self.ratio_foreground_progress_bar = self.percentage_experience_before + \
            self.percentage_experience_won
