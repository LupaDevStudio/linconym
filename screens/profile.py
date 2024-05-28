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
from tools.levels import (
    compute_progression
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
    percentage_experience = NumericProperty()
    lincoins_count = NumericProperty()
    linclues_count = NumericProperty()
    theme_colors = StringProperty()

    classic_mode_achievements = StringProperty()
    # daily_mode_achievements = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.lincoins_count = USER_DATA.user_profile["lincoins"]
        self.linclues_count = USER_DATA.user_profile["linclues"]
        self.user_level = "Level " + str(USER_DATA.user_profile["level"])
        _, self.percentage_experience = compute_progression(
            USER_DATA.user_profile["experience"])
        self.theme_colors = USER_DATA.settings["current_theme_colors"]
        self.user_status = USER_DATA.user_profile["status"].capitalize()
        self.user_status_image = PATH_BADGES + self.user_status.lower() + ".png"

        completed_puzzles = USER_DATA.get_nb_completed_puzzles()
        completed_acts = USER_DATA.get_nb_completed_acts()
        stars_won = USER_DATA.get_nb_total_stars()
        self.classic_mode_achievements = "Completed puzzles: %i\nCompleted acts: %i\nStars won: %i\n\nClick to see all achievements." % (
            completed_puzzles, completed_acts, stars_won)
        # self.daily_mode_achievements = "Completed puzzles: %i\n\nClick to see all achievements." % (
        #     14)

        self.ids.exp_counter.update_experience(None, None)

    def go_to_boosters(self):
        self.go_to_next_screen(screen_name="boosters")

    def open_achievements_classic(self):
        self.go_to_next_screen(screen_name="achievements")

    def open_achievements_daily(self):
        self.go_to_next_screen(screen_name="achievements")

    def open_badges(self):
        self.go_to_next_screen(screen_name="badges")
