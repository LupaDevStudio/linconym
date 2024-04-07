"""
Module to create custom buttons with round transparent white background.
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
    BooleanProperty,
    ObjectProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    LABEL_FONT_SIZE,
    CONTENT_LABEL_FONT_SIZE,
    SMALL_LABEL_FONT_SIZE,
    DISABLE_BUTTON_COLOR
)

#############
### Class ###
#############


class QuestsLayout(RelativeLayout):
    """
    The layout for the quests item.
    """

    background_color = ColorProperty(CUSTOM_BUTTON_BACKGROUND_COLOR)
    primary_color = ColorProperty()
    secondary_color = ColorProperty()
    disable_color = ColorProperty(DISABLE_BUTTON_COLOR)
    text_filling_ratio = NumericProperty(0.8)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    font_size_title = NumericProperty(LABEL_FONT_SIZE)
    font_size_content = NumericProperty(CONTENT_LABEL_FONT_SIZE)
    font_size_reward = NumericProperty(SMALL_LABEL_FONT_SIZE)
    font_ratio = NumericProperty(1)
    level_id = NumericProperty(1)
    description = StringProperty()
    button_text = StringProperty("Go to quest")
    has_completed = BooleanProperty(False)
    has_got_reward = BooleanProperty(False)
    reward = NumericProperty()
    release_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.always_release = True

        self.bind(has_got_reward=self.update_button_text)
        self.bind(has_completed=self.update_button_text)

    def update_button_text(self, base_widget, value):
        if self.has_got_reward:
            self.button_text = "Reward claimed"
        else:
            if self.has_completed:
                self.button_text = "Claim reward"
            else:
                self.button_text = "Go to quest"
