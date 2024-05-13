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
    PATH_BADGES
)
from tools.constants import (
    USER_DATA,
    SCREEN_BOTTOM_BAR,
    SCREEN_TITLE,
    SCREEN_TUTORIAL
)
from screens.custom_widgets import (
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
        SCREEN_TITLE: "Profile",
        SCREEN_BOTTOM_BAR: "profile",
        SCREEN_TUTORIAL: ""
    }

    user_status = StringProperty()
    user_status_image = StringProperty()
    user_level = StringProperty()
    coins_count = NumericProperty()
    theme_colors = StringProperty()

    classic_mode_achievements = StringProperty()
    daily_mode_achievements = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.coins_count = USER_DATA.user_profile["lincoins"]
        self.user_level = "Level " + str(USER_DATA.user_profile["level"])
        self.theme_colors = USER_DATA.settings["current_theme_colors"]
        self.user_status = USER_DATA.user_profile["status"]
        self.user_status_image = PATH_BADGES + self.user_status.lower() + ".png"

        self.classic_mode_achievements = "Completed levels: %i\nCompleted acts: %i\nStars won: %i\n\nClick to see all achievements." % (
            14, 1, 32)
        self.daily_mode_achievements = "Completed levels: %i\n\nClick to see all achievements." % (
            14)

    def go_to_boosters(self):
        self.go_to_next_screen(screen_name="boosters")

    def open_achievements_classic(self):
        self.go_to_next_screen(screen_name="achievements")

    def open_achievements_daily(self):
        self.go_to_next_screen(screen_name="achievements")

    def open_badges(self):
        self.go_to_next_screen(screen_name="badges")
