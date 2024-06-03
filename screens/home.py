"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Python imports ###

from datetime import datetime

### Local imports ###

from tools.constants import (
    SCREEN_TITLE,
    SCREEN_BOTTOM_BAR,
    SCREEN_TUTORIAL,
    USER_DATA
)
from tools import (
    music_mixer
)
from screens.custom_widgets import (
    LinconymScreen,
    DailyWheelPopup
)


#############
### Class ###
#############


class HomeScreen(LinconymScreen):
    """
    Class to manage the home screen which contains the buttons to launch the free and daily modes.
    """

    dict_type_screen = {
        SCREEN_TITLE: "Linconym",
        SCREEN_BOTTOM_BAR: "home",
        SCREEN_TUTORIAL: ""
    }

    def on_enter(self, *args):
        current_music = USER_DATA.settings["current_music"]
        if music_mixer.musics[current_music].state == "stop":
            music_mixer.play(current_music, loop=True)

        today_date = datetime.today().strftime('%m/%d/%Y')
        if USER_DATA.ads["current_day_date"] != today_date:
            USER_DATA.ads["current_day_date"] = today_date
            USER_DATA.ads["number_daily_ads_left"] = 3
            USER_DATA.ads["has_seen_daily_wheel"] = False

        # Don't show the daily wheel on the first connexion
        if not USER_DATA.tutorial["home"]:
            USER_DATA.ads["has_seen_daily_wheel"] = True

        if not USER_DATA.ads["has_seen_daily_wheel"]:
            USER_DATA.ads["has_seen_daily_wheel"] = True
            popup = DailyWheelPopup(
                font_ratio=self.font_ratio,
                primary_color=self.primary_color,
                secondary_color=self.secondary_color
            )
            popup.open()
        USER_DATA.save_changes()
        return super().on_enter(*args)

    def open_classic_mode(self):
        """
        Open the classic mode screen.
        """
        self.manager.go_to_next_screen(next_screen_name="classic_mode")
