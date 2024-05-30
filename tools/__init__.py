"""
Tools package of the application.

Modules
-------

"""

import os

from tools.path import (
    PATH_MUSICS,
    PATH_SOUNDS
)

from tools.constants import (
    USER_DATA
)
from tools.game_tools import (
    MusicMixer,
    DynamicMusicMixer,
    SoundMixer,
    load_sounds
)

MUSIC_DICT = load_sounds(
    [USER_DATA.settings["current_music"] + ".mp3"], PATH_MUSICS, USER_DATA.settings["music_volume"])

SOUND_DICT = load_sounds(os.listdir(PATH_SOUNDS),
                         PATH_SOUNDS, USER_DATA.settings["sound_volume"])

# Create the mixer
music_mixer = DynamicMusicMixer(MUSIC_DICT, USER_DATA.settings["music_volume"])
sound_mixer = DynamicMusicMixer(SOUND_DICT, USER_DATA.settings["sound_volume"])
