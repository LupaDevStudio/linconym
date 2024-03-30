"""
Module referencing the main constants of the application.

Constants
---------
__version__ : str
    Version of the application.

MOBILE_MODE : bool
    Whether the application is launched on mobile or not.
"""

###############
### Imports ###
###############

### Python imports ###

import os

### Kivy imports ###

from kivy import platform

### Local imports ###

from tools.path import (
    PATH_USER_DATA,
    PATH_WORDS_10K,
    PATH_WORDS_34K,
    PATH_WORDS_88K,
    PATH_WORDS_280K,
    PATH_GAMEPLAY,
    PATH_CUSTOMIZATION,
    PATH_RESOURCES,
    PATH_QUESTS,
    PATH_CREDITS,
    PATH_ACHIEVEMENTS
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)

#################
### Constants ###
#################

### Version ###

__version__ = "1.0.0"

### Mode ###

MOBILE_MODE = platform == "android"
DEBUG_MODE = False
FPS = 30
MSAA_LEVEL = 2
BACK_ARROW_SIZE = 0.2

### Data loading ###

# scale for experience awarded to the user
XP_PER_LEVEL: int = 10

# Create the user data json if it does not exist
if not os.path.exists(PATH_USER_DATA):
    default_user_data = {
        "classic_mode": {
            "Act1": {
                "1": {
                    "nb_stars": 3,
                    "best_solution_nb_words": 5,
                    "words_found": [],
                    "position_to_word_id": {},
                    "current_position": ""
                }
            }
        },
        "daily_mode": {
            "start_word": "",
            "end_word": ""
        },
        "achievements": {},
        "quests": {
            "Act1": {}
        },
        "settings": {
            "sound_volume": 0.5,
            "music_volume": 0.5,
            "current_theme_image": "japanese_etching",
            "current_music": "kids_party",
            "current_theme_colors": "japanese_etching"
        },
        "unlocked_themes": {},
        "unlocked_musics": {},
        "user_profile": {
            "status": "Beginner",
            "level": 1,
            "experience": 0,
            "coins": 100000
        },
        "ads": {
            "1": False,
            "2": False,
            "3": False
        }
    }
    save_json_file(PATH_USER_DATA, default_user_data)

# Load the data of the user


class UserData():
    """
    A class to store the user data.
    """

    def __init__(self) -> None:
        data = load_json_file(PATH_USER_DATA)
        self.classic_mode = data["classic_mode"]
        self.daily_mode = data["daily_mode"]
        self.quests = data["quests"]
        self.achievements = data["achievements"]
        self.settings = data["settings"]
        self.unlocked_themes = data["unlocked_themes"]
        self.unlocked_musics = data["unlocked_musics"]
        self.user_profile = data["user_profile"]
        self.ads = data["ads"]

    def save_changes(self) -> None:
        """
        Save the changes in the data.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Create the dictionary of data
        data = {}
        data["classic_mode"] = self.classic_mode
        data["daily_mode"] = self.daily_mode
        data["quests"] = self.quests
        data["achievements"] = self.achievements
        data["settings"] = self.settings
        data["unlocked_themes"] = self.unlocked_themes
        data["unlocked_musics"] = self.unlocked_musics
        data["user_profile"] = self.user_profile
        data["ads"] = self.ads

        # Save this dictionary
        save_json_file(
            file_path=PATH_USER_DATA,
            dict_to_save=data)

    def change_theme_image(self, theme):
        USER_DATA.settings["current_theme_image"] = theme
        self.save_changes()

    def change_theme_colors(self, theme):
        USER_DATA.settings["current_theme_colors"] = theme
        self.save_changes()

    def change_boosters(self, number):
        USER_DATA.ads[str(number)] = True
        self.save_changes()

    def buy_item(self, theme, item_type, price):
        if self.user_profile["coins"] >= price:
            self.user_profile["coins"] = self.user_profile["coins"] - price
            if item_type == "music":
                self.unlocked_musics[theme] = True
            elif item_type == "image":
                if theme not in self.unlocked_themes:
                    self.unlocked_themes[theme] = {
                        "image": False,
                        "colors": False}
                self.unlocked_themes[theme]["image"] = True
            elif item_type == "colors":
                if theme not in self.unlocked_themes:
                    self.unlocked_themes[theme] = {
                        "image": False,
                        "colors": False}
                self.unlocked_themes[theme]["colors"] = True
            else:
                raise ValueError("Unrecognized item type.")
            self.save_changes()
            return True
        return False


USER_DATA = UserData()

### Tutorial ###

TUTORIAL = load_json_file(PATH_RESOURCES + "tutorial.json")

### Colors ###

class ColorPalette():
    """
    Class to store the colors used in the screens.
    """

    def __init__(self) -> None:
        self.PRIMARY = (0, 0, 0, 1)
        self.SECONDARY = (0, 0, 0, 1)

CUSTOM_BUTTON_BACKGROUND_COLOR = (1, 1, 1, 0.7)
DISABLE_BUTTON_COLOR = (0.15, 0.15, 0.15, 1)
OPACITY_ON_BUTTON_PRESS = 0.8
RATE_CHANGE_OPACITY = 0.05

### Font sizes, outlines and colors ###

TITLE_FONT_SIZE = 45
TITLE_OUTLINE_COLOR = (1, 1, 1, 1)
TITLE_OUTLINE_WIDTH = 2

LABEL_FONT_SIZE = 28
SMALL_LABEL_FONT_SIZE = 22
CONTENT_LABEL_FONT_SIZE = 17

MAIN_BUTTON_FONT_SIZE = 30
BUTTON_FONT_SIZE = 20
SMALL_BUTTON_FONT_SIZE = 15
BUTTON_OUTLINE_WIDTH = 1.5

ACT_BUTTON_FONT_SIZE = 25
CUSTOMIZATION_LAYOUT_FONT_SIZE = 20
COINS_COUNT_FONT_SIZE = 22
EXPERIENCE_FONT_SIZE = 15
LEVEL_ID_FONT_SIZE = 22
LETTER_FONT_SIZE = 18

BIG_BUYING_BUTTON_FONT_SIZE = 25
SMALL_BUYING_BUTTON_FONT_SIZE = 18


TEXT_FONT_COLOR = (0, 0, 0, 1)

### Spacing and heights ###

BOTTOM_BAR_HEIGHT = 0.12

# Pos hints for icon buttons
POS_HINT_LEFT_TOP_BUTTON = {"x": 0.02, "top": 0.99}
POS_HINT_RIGHT_TOP_BUTTON = {"right": 0.98, "top": 0.99}
POS_HINT_RIGHT_BOTTOM_BUTTON = {"right": 0.98, "y": 0.01}

# Levels configuration
MAX_NB_LEVELS_PER_BRANCH = 4
LEVEL_BUTTON_SIZE_HINT = 0.15
LEVEL_BUTTON_RELATIVE_HEIGHT = 0.4
LEVEL_BRANCH_RELATIVE_HEIGHT = 0.2
LEVEL_BUTTON_SPACING = (1 - (MAX_NB_LEVELS_PER_BRANCH + 1)
                        * LEVEL_BUTTON_SIZE_HINT) / MAX_NB_LEVELS_PER_BRANCH
LEVEL_BUTTON_SIDE_OFFSET = LEVEL_BUTTON_SIZE_HINT + LEVEL_BUTTON_SPACING

WORD_BUTTON_WIDTH_HINT = 0.3
WORD_BUTTON_HEIGHT_HINT = 0.1
WORD_BUTTON_VSPACING = 0.05
WORD_BUTTON_HSPACING = 0.1
WORD_BUTTON_SIDE_OFFSET = 0.1

### Screens ###

SCREEN_TITLE = "has_title"
SCREEN_BACK_ARROW = "has_back_arrow"
SCREEN_BOTTOM_BAR = "has_bottom_bar_"
SCREEN_TUTORIAL = "has_tutorial"

### Ads code ###

DICT_AMOUNT_ADS = {
    "1": 100,
    "2": 50,
    "3": 30
}
REWARD_INTERSTITIAL = ""
INTERSTITIAL = ""

### Buy items ###

DICT_AMOUNT_BUY = {
    "1": {
        "amount": 1000,
        "price": 1
    },
    "2": {
        "amount": 6000,
        "price": 5
    },
    "3": {
        "amount": 15000,
        "price": 10
    }
}

### Words loading ###

with open(PATH_WORDS_10K) as file:
    ENGLISH_WORDS_10K = []
    for i, line in enumerate(file):
        ENGLISH_WORDS_10K.append(line.replace("\n", ""))

with open(PATH_WORDS_34K) as file:
    ENGLISH_WORDS_34K = []
    for i, line in enumerate(file):
        ENGLISH_WORDS_34K.append(line.replace("\n", ""))

with open(PATH_WORDS_88K) as file:
    ENGLISH_WORDS_88K = []
    for i, line in enumerate(file):
        ENGLISH_WORDS_88K.append(line.replace("\n", ""))

with open(PATH_WORDS_280K) as file:
    ENGLISH_WORDS_280K = []
    for i, line in enumerate(file):
        ENGLISH_WORDS_280K.append(line.replace("\n", ""))

DICT_ID_LIST: list[str] = ["10k", "34k", "88k", "280k"]
NB_DICTS: int = len(DICT_ID_LIST)

ENGLISH_WORDS_DICTS = {
    DICT_ID_LIST[0]: ENGLISH_WORDS_10K,
    DICT_ID_LIST[1]: ENGLISH_WORDS_34K,
    DICT_ID_LIST[2]: ENGLISH_WORDS_88K,
    DICT_ID_LIST[3]: ENGLISH_WORDS_280K
}

DICT_ID_TO_NB_WORDS = {
    DICT_ID_LIST[0]: 10000,
    DICT_ID_LIST[1]: 34000,
    DICT_ID_LIST[2]: 88000,
    DICT_ID_LIST[3]: 375000
}

### Levels, quests and achievements ###

GAMEPLAY_DICT = load_json_file(PATH_GAMEPLAY)
QUESTS_DICT = load_json_file(PATH_QUESTS)
CREDITS_DICT = load_json_file(PATH_CREDITS)
ACHIEVEMENTS_DICT = load_json_file(PATH_ACHIEVEMENTS)

### Customization with themes and musics ###

CUSTOMIZATION_DICT = load_json_file(PATH_CUSTOMIZATION)
THEMES_DICT = CUSTOMIZATION_DICT["themes"]
MUSICS_DICT = CUSTOMIZATION_DICT["musics"]
