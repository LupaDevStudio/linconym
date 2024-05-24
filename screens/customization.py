"""
Module to create the customization screen.
"""

###############
### Imports ###
###############

from tools.constants import (
    SCREEN_TITLE,
    SCREEN_BOTTOM_BAR
)
from screens.custom_widgets import (
    LinconymScreen
)
from tools import (
    music_mixer
)


#############
### Class ###
#############


class CustomizationScreen(LinconymScreen):
    """
    Class to manage the customization screen which allows the user to choose between themes or music.
    """

    dict_type_screen = {
        SCREEN_TITLE: "Customization",
        SCREEN_BOTTOM_BAR: "customization"
    }

    def open_musics_screen(self, *_):
        self.go_to_next_screen(screen_name="musics")

    def open_themes_screen(self, *_):
        self.go_to_next_screen(screen_name="themes")
