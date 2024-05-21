"""
Module to create the settings screen.
"""

###############
### Imports ###
###############

### Python imports ###

import webbrowser

### Kivy imports ###

from kivy.properties import StringProperty

### Local imports ###

from tools.constants import (
    USER_DATA,
    __version__,
    SCREEN_TITLE,
    SCREEN_BOTTOM_BAR,
    SCREEN_TUTORIAL
)
from screens.custom_widgets import (
    LinconymScreen
)
from tools import (
    music_mixer,
    sound_mixer
)

#############
### Class ###
#############


class SettingsScreen(LinconymScreen):
    """
    Class to manage the settings screen.
    """

    dict_type_screen = {
        SCREEN_TITLE: "Settings",
        SCREEN_BOTTOM_BAR: "settings",
        SCREEN_TUTORIAL: ""
    }
    version_text = StringProperty()
    keyboard_mode = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.version_text = "Version " + str(__version__)
        self.keyboard_mode = USER_DATA.settings["keyboard_mode"]
        self.ids.sound_slider.bind(value=self.update_sound_volume)
        self.ids.music_slider.bind(value=self.update_music_volume)

    def on_pre_enter(self, *args):
        return super().on_pre_enter(*args)

    def on_leave(self, *args):
        USER_DATA.save_changes()
        return super().on_leave(*args)

    def update_sound_volume(self, widget, value):
        sound_volume = value
        sound_mixer.change_volume(sound_volume)
        USER_DATA.settings["sound_volume"] = sound_volume

    def update_music_volume(self, widget, value):
        music_volume = value
        music_mixer.change_volume(music_volume)
        USER_DATA.settings["music_volume"] = music_volume

    def change_keyboard_mode(self):
        USER_DATA.settings["keyboard_mode"] = self.ids.keyboard_spinner.text

    def open_credits(self):
        self.manager.go_to_next_screen("credits")

    def open_lupa_website(self):
        """
        Open LupaDevStudio website.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        webbrowser.open("https://lupadevstudio.com", 2)
