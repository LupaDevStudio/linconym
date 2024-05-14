"""
Module to store all the paths used for the app files and folders
"""

###############
### Imports ###
###############

from kivy.utils import platform

#################
### Constants ###
#################

MOBILE_MODE = platform == "android"

if MOBILE_MODE:
    from android.storage import app_storage_path  # pylint: disable=import-error # type: ignore
    PATH_APP_FOLDER = app_storage_path() + "/"
else:
    PATH_APP_FOLDER = "./"

# Path for the folders
PATH_RESOURCES = "resources/"

# Path for the user data
PATH_USER_DATA = PATH_APP_FOLDER + "data.json"

# Path for the screen
PATH_SCREENS = "screens/"

# Path for the resources
PATH_IMAGES = PATH_RESOURCES + "images/"
PATH_BACKGROUNDS = PATH_IMAGES + "backgrounds/"
PATH_ANIMATED_BACKGROUNDS = PATH_IMAGES + "animated_backgrounds/"
PATH_BADGES = PATH_IMAGES + "badges/"
PATH_ICONS = PATH_IMAGES + "icons/"
PATH_TEMP_IMAGES = PATH_IMAGES + "temp/"
PATH_SOUNDS = PATH_RESOURCES + "sounds/"
PATH_MUSICS = PATH_RESOURCES + "musics/"
PATH_FONTS = PATH_RESOURCES + "fonts/"
PATH_GAMEPLAY = PATH_RESOURCES + "gameplay.json"
PATH_QUESTS = PATH_RESOURCES + "quests.json"
PATH_ACHIEVEMENTS = PATH_RESOURCES + "achievements.json"
PATH_CUSTOMIZATION = PATH_RESOURCES + "customization.json"
PATH_USER_STATUS = PATH_RESOURCES + "user_status.json"
PATH_DICTIONNARIES = PATH_RESOURCES + "dictionnaries/"
PATH_CREDITS = "licenses/credits.json"
PATH_WORDS_280K = PATH_DICTIONNARIES + "english_words_280k.txt"
PATH_WORDS_10K = PATH_DICTIONNARIES + "english_words_10k.txt"
PATH_WORDS_34K = PATH_DICTIONNARIES + "english_words_34k.txt"
PATH_WORDS_88K = PATH_DICTIONNARIES + "english_words_88k.txt"

# Path for the fonts
PATH_TEXT_FONT = PATH_FONTS + "Oxanium-Bold.ttf"
PATH_TITLE_FONT = PATH_FONTS + "Oxanium-ExtraBold.ttf"
