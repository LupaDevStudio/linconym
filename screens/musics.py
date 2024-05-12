"""
Module to create the musics screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.core.audio import SoundLoader
from kivy.properties import (
    NumericProperty
)

### Local imports ###

from tools.path import PATH_MUSICS
from tools.constants import (
    USER_DATA,
    MUSICS_DICT,
    SCREEN_TITLE,
    SCREEN_BACK_ARROW,
    SCREEN_BOTTOM_BAR,
    SCREEN_TUTORIAL
)
from tools import (
    music_mixer
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
    Class to manage the screen that contains the customization for musics.
    """

    dict_type_screen = {
        SCREEN_TITLE: "Musics",
        SCREEN_BOTTOM_BAR: "none",
        SCREEN_BACK_ARROW: "",
        SCREEN_TUTORIAL: ""
    }

    coins_count = NumericProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.coins_count = USER_DATA.user_profile["lincoins"]
        super().on_pre_enter(*args)
        self.fill_scrollview()

    def on_leave(self, *args):
        super().on_leave(*args)

        # When leaving the screen re-enable the music chosen by the user
        self.play_current_user_music()

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()

    def go_to_boosters(self):
        self.go_to_next_screen(screen_name="boosters")

    def stop_playing_all_musics(self):
        for music_layout_key in self.MUSICS_LAYOUT_DICT:
            music_layout: MusicLayout = self.MUSICS_LAYOUT_DICT[music_layout_key]
            music_layout.is_playing = False

    def deselect_all_musics(self):
        for music_layout_key in self.MUSICS_LAYOUT_DICT:
            music_layout: MusicLayout = self.MUSICS_LAYOUT_DICT[music_layout_key]
            music_layout.is_using_music = False

    def play_current_user_music(self):
        current_music = USER_DATA.settings["current_music"]
        if music_mixer.musics[current_music].state == "stop":
            music_mixer.play(current_music, loop=True)

    def change_current_user_music(self, new_music):
        USER_DATA.settings["current_music"] = new_music
        if new_music not in USER_DATA.unlocked_musics:
            USER_DATA.unlocked_musics.append(new_music)
        USER_DATA.save_changes()
        if new_music not in music_mixer.musics:
            new_music_sound = SoundLoader.load(
                PATH_MUSICS + new_music + ".mp3")
            music_mixer.add_sound(new_music_sound, new_music)
        music_mixer.play(new_music, loop=True)

    def fill_scrollview(self):
        scrollview_layout = self.ids.scrollview_layout
        layout_height = 75

        # Store the widgets
        self.MUSICS_LAYOUT_DICT = {}
        for music in MUSICS_DICT:
            has_bought_music = music in USER_DATA.unlocked_musics
            is_using_music = USER_DATA.settings["current_music"] == music
            current_music_layout = MusicLayout(
                music_title=MUSICS_DICT[music]["name"],
                music_price=MUSICS_DICT[music]["price"],
                music_source=MUSICS_DICT[music]["source"].replace(".mp3", ""),
                music_id=music,
                font_ratio=self.font_ratio * 0.8,
                primary_color=self.primary_color,
                has_bought_music=has_bought_music,
                is_using_music=is_using_music,
                disable_button=True,
                size_hint_y=None,
                height=layout_height * self.font_ratio,
                stop_playing_other_layouts=self.stop_playing_all_musics,
                change_current_user_music=self.change_current_user_music,
                play_current_user_music=self.play_current_user_music,
                deselect_all_musics=self.deselect_all_musics
            )
            current_music_layout.update_display()
            self.MUSICS_LAYOUT_DICT[music] = current_music_layout
            scrollview_layout.add_widget(current_music_layout)

    def update_coins(self):
        self.coins_count = USER_DATA.user_profile["lincoins"]