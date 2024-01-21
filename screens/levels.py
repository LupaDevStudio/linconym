"""
Module to create the levels screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import ColorProperty

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS
)
from tools.constants import (
    USER_DATA,
    THEMES_DICT
)
from tools.kivy_tools import (
    ImprovedScreen
)
from tools import (
    music_mixer
)


#############
### Class ###
#############


class LevelsScreen(ImprovedScreen):
    """
    Class to manage the levels screen which allow the user to select a level inside an act.
    """

    primary_color = ColorProperty((0, 0, 0, 1))
    secondary_color = ColorProperty((0, 0, 0, 1))

    def __init__(self, **kwargs) -> None:
        current_theme_image = USER_DATA.settings["current_theme_image"]
        super().__init__(
            back_image_path=PATH_BACKGROUNDS +
            THEMES_DICT[current_theme_image]["image"],
            **kwargs)
        self.current_act_id = ""

    def on_pre_enter(self, *args):
        current_theme_colors = USER_DATA.settings["current_theme_colors"]
        self.primary_color = THEMES_DICT[current_theme_colors]["primary"]
        self.secondary_color = THEMES_DICT[current_theme_colors]["secondary"]
        self.ids.level_layout.act_id = self.current_act_id
        self.ids.level_layout.build_layout()
        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.ids.level_layout.clear_widgets()
        return super().on_leave(*args)

    def open_game_screen(self):
        self.manager.get_screen("game").current_act_id = self.current_act_id
        self.manager.current = "game"