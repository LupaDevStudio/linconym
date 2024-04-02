"""
Module to create the musics screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    NumericProperty
)

### Local imports ###

from tools.constants import (
    USER_DATA,
    THEMES_DICT,
    MUSICS_DICT,
    SCREEN_TITLE,
    SCREEN_BACK_ARROW,
    SCREEN_BOTTOM_BAR,
    SCREEN_TUTORIAL
)
from screens.custom_widgets import (
    LinconymScreen
)
from screens import (
    MusicLayout
)

#############
### Class ###
#############


class MusicsScreen(LinconymScreen):
    """
    Class to manage the screen that contains the profile information.
    """

    dict_type_screen = {
        SCREEN_TITLE: "Musics",
        SCREEN_BOTTOM_BAR: "none",
        SCREEN_BACK_ARROW: "",
        SCREEN_TUTORIAL: ""
    }

    coins_count = NumericProperty()

    def on_pre_enter(self, *args):
        self.coins_count = USER_DATA.user_profile["coins"]
        super().on_pre_enter(*args)
        self.fill_scrollview()

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()

    def go_to_boosters(self):
        self.go_to_next_screen(screen_name="boosters")

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]
        # Load the widgets
        self.MUSICS_LAYOUT_DICT = {}
        for music in MUSICS_DICT:
            has_bought_music = USER_DATA.unlocked_musics[music]
            is_using_music = USER_DATA.settings["current_music"] == music
            current_music_layout = MusicLayout(
                music_title=MUSICS_DICT[music]["name"],
                music_price=MUSICS_DICT[music]["price"],
                font_ratio=self.font_ratio * 0.8,
                primary_color=self.primary_color,
                has_bought_music=has_bought_music,
                is_using_music=is_using_music,
                disable_button=True,
                height=50)
            current_music_layout.update_display()
            self.MUSICS_LAYOUT_DICT[music] = current_music_layout
            scrollview_layout.add_widget(current_music_layout)
