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
from typing import Literal

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
    PATH_ACHIEVEMENTS,
    PATH_ICONS,
    PATH_USER_STATUS
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)

#################
### Constants ###
#################

### Version ###

__version__ = "0.1.0"

### Mode ###

MOBILE_MODE = platform == "android"
DEBUG_MODE = False
FPS = 30
MSAA_LEVEL = 2
BACK_ARROW_SIZE = 0.2

### Data loading ###

# scale for experience awarded to the user
XP_PER_LEVEL: int = 100

# Create the user data json if it does not exist
if not os.path.exists(PATH_USER_DATA):
    default_user_data = {
        "classic_mode": {
            "1": {
                "1": {
                    "nb_stars": 0
                }
            }
        },
        "daily_mode": {
            "start_word": "",
            "end_word": ""
        },
        "achievements": {},
        "quests": {
            "1": {}
        },
        "settings": {
            "sound_volume": 0.5,
            "music_volume": 0.5,
            "keyboard_mode": "QWERTY",
            "current_theme_image": "lupa",
            "current_music": "inspiring",
            "current_theme_colors": "lupa",
            "hide_completed_branches": False
        },
        "unlocked_themes": {
            "lupa": {
                "image": True,
                "colors": True
            }
        },
        "unlocked_musics": ["inspiring"],
        "user_profile": {
            "status": "novice",
            "level": 1,
            "experience": 0,
            "lincoins": 0,
            "linclues": 0,
            "cumulated_lincoins": 0,
            "cumulated_linclues": 0
        },
        "tutorial": {
            "home": False,
            "profile": False,
            "settings": False,
            "levels": True,
            "game": {
                "change_letter": False,
                "delete_letter": False,
                "add_letter": False,
                "practice": False,
                "reorganize_letters": False,
                "all_rules": True
            },
            "themes": True,
            "boosters": False,
            "musics": True,
            "achievements": True,
            "quests": True,
            "configure_tree": True
        },
        "ads": {
            "current_day_date": "06/09/2024",
            "current_week_date": "06/03/2024",
            "number_daily_ads_left": 3,
            "number_weekly_ads_left": 1
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
        self.tutorial = data["tutorial"]
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
        data["tutorial"] = self.tutorial
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

    def change_boosters(self, mode: Literal["daily", "weekly"]):
        USER_DATA.ads[f"number_{mode}_ads_left"] -= 1
        self.save_changes()

    def get_nb_total_stars(self):
        """
        Compute the total number of stars gathered by the user.

        Returns
        -------
        int
            Number of stars gathered by the user.
        """

        total_nb_stars = 0
        for act in USER_DATA.classic_mode:
            for level in USER_DATA.classic_mode[act]:
                total_nb_stars += USER_DATA.classic_mode[act][level]["nb_stars"]

        return total_nb_stars

    def get_mean_nb_stars_on_act(self, act_id):
        """
        Compute the mean number of stars on the given act.

        Parameters
        ----------
        act_id : str
            Id of the act.

        Returns
        -------
        int
        """

        # Check if the user has already played on the level
        if act_id not in USER_DATA.classic_mode:
            return 0

        total_nb_stars = 0
        nb_levels = 0

        for level in GAMEPLAY_DICT[act_id]:
            if level in USER_DATA.classic_mode[act_id]:
                total_nb_stars += USER_DATA.classic_mode[act_id][level]["nb_stars"]
            nb_levels += 1

        mean = total_nb_stars / nb_levels

        return int(mean)

    def get_nb_completed_levels_for_act(self, act_id: str):
        """
        Compute the number of completed levels on the given act.

        Parameters
        ----------
        act_id : str
            Id of the act.

        Returns
        -------
        int
            Number of levels already completed.
        """

        # Check if the user has already played on the level
        if act_id not in USER_DATA.classic_mode:
            return 0

        # Allocate a variable for the output
        nb_completed_levels = 0

        # Iterate over the saved data to count the levels
        for level_id in USER_DATA.classic_mode[act_id]:
            if USER_DATA.classic_mode[act_id][level_id]["nb_stars"] > 0:
                nb_completed_levels += 1

        return nb_completed_levels

    def buy_item(self, theme, item_type, price):
        if self.user_profile["lincoins"] >= price:
            self.user_profile["lincoins"] = self.user_profile["lincoins"] - price
            if item_type == "music":
                self.unlocked_musics.append(theme)
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
GAME_TUTORIAL_DICT = {
    "1": "change_letter",
    "2": "delete_letter",
    "3": "add_letter",
    "4": "practice",
    "5": "reorganize_letters"
}

### Colors ###


class ColorPalette():
    """
    Class to store the colors used in the screens.
    """

    def __init__(self) -> None:
        self.PRIMARY = (0, 0, 0, 1)
        self.SECONDARY = (0, 0, 0, 1)


CUSTOM_BUTTON_BACKGROUND_COLOR = (1, 1, 1, 0.7)
CLOUD_GREY_BACKGROUND_COLOR = (0.8, 0.8, 0.8, 0.7)
DISABLE_BUTTON_COLOR = (0.15, 0.15, 0.15, 1)
OPACITY_ON_BUTTON_PRESS = 0.8
RATE_CHANGE_OPACITY = 0.05

### Font sizes, outlines and colors ###

TITLE_FONT_SIZE = 38
TITLE_OUTLINE_COLOR = (1, 1, 1, 1)
TITLE_OUTLINE_WIDTH = 2

LABEL_FONT_SIZE = 22
SMALL_LABEL_FONT_SIZE = 18
CONTENT_LABEL_FONT_SIZE = 14

MAIN_BUTTON_FONT_SIZE = 25
BUTTON_FONT_SIZE = 20
SMALL_BUTTON_FONT_SIZE = 15
BUTTON_OUTLINE_WIDTH = 1

SPINNER_BUTTON_FONT_SIZE = 20

ACT_BUTTON_FONT_SIZE = 22
CUSTOMIZATION_LAYOUT_FONT_SIZE = 15
COINS_COUNT_FONT_SIZE = 20
EXPERIENCE_FONT_SIZE = 15
LEVEL_ID_FONT_SIZE = 22
LETTER_FONT_SIZE = 18

CREDITS_SCROLLVIEW_FONT_SIZE = 25
CREDITS_CONTENT_SCROLLVIEW_FONT_SIZE = 15

TEXT_FONT_COLOR = (0, 0, 0, 1)

### Spacing and heights ###

BOTTOM_BAR_HEIGHT = 0.12

# Pos hints for icon buttons
POS_HINT_LEFT_TOP_BUTTON = {"x": 0.02, "top": 0.99}
POS_HINT_RIGHT_TOP_BUTTON = {"right": 0.98, "top": 0.99}
POS_HINT_LEFT_BOTTOM_BUTTON = {"x": 0.02, "y": 0.01}
POS_HINT_RIGHT_BOTTOM_BUTTON = {"right": 0.98, "y": 0.01}

# Levels configuration
MAX_NB_LEVELS_PER_BRANCH = 4
LEVEL_BUTTON_SIZE_HINT = 0.15
LEVEL_BUTTON_RELATIVE_HEIGHT = 0.4
LEVEL_BRANCH_RELATIVE_HEIGHT = 0.2
LEVEL_BUTTON_SPACING = (1 - (MAX_NB_LEVELS_PER_BRANCH + 1)
                        * LEVEL_BUTTON_SIZE_HINT) / MAX_NB_LEVELS_PER_BRANCH
LEVEL_BUTTON_SIDE_OFFSET = LEVEL_BUTTON_SIZE_HINT + LEVEL_BUTTON_SPACING

# The spacing is expressed as a proportion of the size of a word button
WORD_BUTTON_VSPACING = 0.25
WORD_BUTTON_HSPACING = 0.33
WORD_BUTTON_SIDE_VOFFSET = 0.33
WORD_BUTTON_SIDE_HOFFSET = 0.33

# Use the spacing to define the hint ref size of a block
WORD_BUTTON_BLOCK_WIDTH_HINT = 1 + WORD_BUTTON_HSPACING
WORD_BUTTON_BLOCK_HEIGHT_HINT = 1 + WORD_BUTTON_VSPACING


### Screens ###

SCREEN_TITLE = "has_title"
SCREEN_BACK_ARROW = "has_back_arrow"
SCREEN_BOTTOM_BAR = "has_bottom_bar_"
SCREEN_TUTORIAL = "has_tutorial"

### Ads code ###

AMOUNT_DAILY_ADS = [
    {
        "lincoin": 80
    },
    {
        "lincoin": 40,
        "linclue": 1
    },
    {
        "linclue": 2
    }
]
AMOUNT_WEEKLY_AD = [{
    "lincoin": 480,
    "linclue": 12
}]
REWARD_INTERSTITIAL = ""
INTERSTITIAL = ""

### Conversion money ###

DICT_CONVERSION_MONEY = {
    "price_lincoins": 50,
    "reward_linclues": 1
}

### Buy items ###

DICT_AMOUNT_BUY = {
    "1": {
        "reward": 1000,
        "price": 1
    },
    "2": {
        "reward": 6000,
        "price": 5
    },
    "3": {
        "reward": 15000,
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
THEMES_RARITY_DICT = CUSTOMIZATION_DICT["categories"]
NB_LINCOINS_PER_STAR_DICT = {
    3: 100,
    2: 70,
    1: 50,
    0: 0
}

### User status ###

USER_STATUS_DICT = load_json_file(PATH_USER_STATUS)

### Lincoins images given the amount of Lincoins ###

def get_lincoin_image_amount(number_lincoins):
    if number_lincoins <= 800:
        return PATH_ICONS + "lincoin_1.png"
    if number_lincoins <= 2000:
        return PATH_ICONS + "lincoin_2.png"
    if number_lincoins <= 4000:
        return PATH_ICONS + "lincoin_3.png"
    if number_lincoins <= 6000:
        return PATH_ICONS + "lincoin_4.png"
    else:
        return PATH_ICONS + "lincoin_5.png"
