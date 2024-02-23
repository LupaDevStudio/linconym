"""
Module to create the profile screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS,
    PATH_BADGES
)
from tools.constants import (
    USER_DATA,
    THEMES_DICT,
    SCREEN_BOTTOM_BAR,
    SCREEN_TITLE
)
from tools.kivy_tools import (
    LinconymScreen
)


#############
### Class ###
#############


class ProfileScreen(LinconymScreen):
    """
    Class to manage the screen that contains the profile information.
    """

    dict_type_screen = {
        SCREEN_TITLE : "Profile",
        SCREEN_BOTTOM_BAR : "profile"
    }

    user_status = StringProperty()
    user_status_image = StringProperty()
    user_level = StringProperty()
    coins_count = NumericProperty()
    theme_colors = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.coins_count = USER_DATA.user_profile["coins"]
        self.user_level = "Level " + str(USER_DATA.user_profile["level"])
        self.theme_colors = USER_DATA.settings["current_theme_colors"]
        self.user_status = USER_DATA.user_profile["status"]
        self.user_status_image = PATH_BADGES + self.user_status.lower() + ".png"
        return super().on_enter(*args)

    def go_to_boosters(self):
        self.manager.go_to_next_screen(next_screen_name="boosters")
