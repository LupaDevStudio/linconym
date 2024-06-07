"""
Module referencing the main constants of the application.

Constants
---------
__version__ : str
    Version of the application.

ANDROID_MODE : bool
    Whether the application is launched on mobile or not.
"""

###############
### Imports ###
###############

### Python imports ###

import os
from typing import Literal


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
    PATH_USER_STATUS,
    PATH_GAMEPLAY_LEGEND,
    IOS_MODE,
    ANDROID_MODE
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)

#################
### Constants ###
#################

### Version ###

__version__ = "1.1.0"

### Mode ###


DEBUG_MODE = False
FPS = 30
MSAA_LEVEL = 2
BACK_ARROW_SIZE = 0.2

### Data loading ###

# scale for experience awarded to the user
XP_PER_CLASSIC_PUZZLE: int = 100
XP_PER_LEGEND_PUZZLE: int = 200
LINCOINS_PER_LEVEL: int = 100

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
        "legend_mode": {
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
            "sound_volume": 1.0,
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
                "more_complicated_puzzles": False,
                "all_rules": True
            },
            "legend_mode": False,
            "themes": True,
            "boosters": False,
            "musics": True,
            "achievements": True,
            "quests": True,
            "configure_tree": True
        },
        "ads": {
            "current_day_date": "",
            "current_week_date": "",
            "number_daily_ads_left": 3,
            "number_weekly_ads_left": 1,
            "has_seen_daily_wheel": False
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
        if "legend_mode" not in data:
            self.legend_mode = {
                "1": {
                    "1": {
                        "nb_stars": 0
                    }
                }
            }
        else:
            self.legend_mode = data["legend_mode"]
        self.daily_mode = data["daily_mode"]
        self.quests = data["quests"]
        self.achievements = data["achievements"]
        self.settings = data["settings"]
        self.unlocked_themes = data["unlocked_themes"]
        self.unlocked_musics = data["unlocked_musics"]
        self.user_profile = data["user_profile"]
        self.tutorial = data["tutorial"]
        if "legend_mode" not in self.tutorial:
            self.tutorial["legend_mode"] = False
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
        data["legend_mode"] = self.legend_mode
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

    def change_boosters(self, mode: Literal["daily", "weekly", "unlimited"]):
        if mode != "unlimited":
            USER_DATA.ads[f"number_{mode}_ads_left"] -= 1
            self.save_changes()

    def get_nb_total_stars(self, mode="classic"):
        """
        Compute the total number of stars gathered by the user.

        Parameters
        ----------
        mode: str, optional (default is "classic")
            Mode of game.

        Returns
        -------
        int
            Number of stars gathered by the user.
        """

        total_nb_stars = 0
        if mode == "classic":
            for act in USER_DATA.classic_mode:
                for level in USER_DATA.classic_mode[act]:
                    total_nb_stars += USER_DATA.classic_mode[act][level]["nb_stars"]
        elif mode == "legend":
            for act in USER_DATA.legend_mode:
                for level in USER_DATA.legend_mode[act]:
                    total_nb_stars += USER_DATA.legend_mode[act][level]["nb_stars"]

        return total_nb_stars

    def get_mean_nb_stars_on_act(self, act_id, mode="classic"):
        """
        Compute the mean number of stars on the given act.

        Parameters
        ----------
        act_id : str
            Id of the act.
        mode: str, optional (default is "classic")
            Mode of game.

        Returns
        -------
        int
        """
        # Check if the user has already played on the level
        if mode == "classic":
            if act_id not in USER_DATA.classic_mode:
                return 0
        elif mode == "legend":
            if act_id not in USER_DATA.legend_mode:
                return 0

        total_nb_stars = 0
        nb_levels = 0

        if mode == "classic":
            for level in GAMEPLAY_DICT[act_id]:
                if level != "name":
                    if level in self.classic_mode[act_id]:
                        total_nb_stars += self.classic_mode[act_id][level]["nb_stars"]
                    nb_levels += 1
        elif mode == "legend":
            for level in GAMEPLAY_LEGEND_DICT[act_id]:
                if level != "name":
                    if level in self.legend_mode[act_id]:
                        total_nb_stars += self.legend_mode[act_id][level]["nb_stars"]
                    nb_levels += 1

        mean = total_nb_stars / nb_levels

        return int(mean)

    def get_nb_completed_puzzles(self, mode="classic"):
        """
        Compute the number of completed puzzles.

        Parameters
        ----------
        mode: str, optional (default is "classic")
            Mode of game.

        Returns
        -------
        int
            Number of puzzles already completed.
        """
        nb_completed_puzzles = 0

        if mode == "classic":
            for act_id in self.classic_mode:
                nb_completed_puzzles += self.get_nb_completed_levels_for_act(
                    act_id)
        elif mode == "legend":
            for act_id in self.legend_mode:
                nb_completed_puzzles += self.get_nb_completed_levels_for_act(
                    act_id, mode=mode)

        return nb_completed_puzzles

    def get_nb_completed_acts(self, mode="classic"):
        """
        Compute the number of completed acts.

        Parameters
        ----------
        mode: str, optional (default is "classic")
            Mode of game.

        Returns
        -------
        int
            Number of acts already completed.
        """
        nb_completed_acts = 0

        if mode == "classic":

            for act_id in self.classic_mode:
                has_finished_act = True

                for puzzle in GAMEPLAY_DICT[act_id]:
                    if puzzle != "name":
                        if puzzle not in self.classic_mode[act_id]:
                            has_finished_act = False
                        elif self.classic_mode[act_id][puzzle]["nb_stars"] == 0:
                            has_finished_act = False

                if has_finished_act:
                    nb_completed_acts += 1

        elif mode == "legend":

            for act_id in self.legend_mode:
                has_finished_act = True

                for puzzle in GAMEPLAY_LEGEND_DICT[act_id]:
                    if puzzle != "name":
                        if puzzle not in self.legend_mode[act_id]:
                            has_finished_act = False
                        elif self.legend_mode[act_id][puzzle]["nb_stars"] == 0:
                            has_finished_act = False

                if has_finished_act:
                    nb_completed_acts += 1

        return nb_completed_acts

    def get_nb_completed_levels_for_act(self, act_id: str, mode="classic"):
        """
        Compute the number of completed levels on the given act.

        Parameters
        ----------
        act_id : str
            Id of the act.
        mode: str, optional (default is "classic")
            Mode of game.

        Returns
        -------
        int
            Number of levels already completed.
        """

        # Check if the user has already played on the level
        if mode == "classic":
            if act_id not in self.classic_mode:
                return 0
        elif mode == "legend":
            if act_id not in self.legend_mode:
                return 0

        # Allocate a variable for the output
        nb_completed_levels = 0

        # Iterate over the saved data to count the levels
        if mode == "classic":
            for level_id in self.classic_mode[act_id]:
                if self.classic_mode[act_id][level_id]["nb_stars"] > 0:
                    nb_completed_levels += 1
        elif mode == "legend":
            for level_id in self.legend_mode[act_id]:
                if self.legend_mode[act_id][level_id]["nb_stars"] > 0:
                    nb_completed_levels += 1

        return nb_completed_levels

    def get_nb_levels_in_act(self, act_id: str, mode="classic"):
        """
        Compute the number of levels contained in an act.

        Parameters
        ----------
        act_id : str
            Id of the act.
        mode: str, optional (default is "classic")
            Mode of game.

        Returns
        -------
        int
            Number of levels.
        """
        current_dict = GAMEPLAY_DICT
        if mode == "legend":
            current_dict = GAMEPLAY_LEGEND_DICT

        if act_id not in current_dict:
            return 0
        else:
            return len(current_dict[act_id]) - 1

    def get_nb_levels_in_all_previous_acts(self, act_id: str, mode="classic"):
        """
        Compute the number of levels contained in all previous acts.

        Parameters
        ----------
        act_id : str
            Id of the act.
        mode: str, optional (default is "classic")
            Mode of game.

        Returns
        -------
        int
            Number of cumulated levels in the previous acts.
        """

        act = int(act_id)
        cum_nb_levels = 0
        for i in range(1, act):
            nb_levels = self.get_nb_levels_in_act(str(i), mode=mode)
            cum_nb_levels += nb_levels

        return cum_nb_levels

    def get_nb_words_all_puzzles(self, word_to_find: str, mode="classic"):
        nb_words = 0

        if mode == "classic":

            for act_id in self.classic_mode:
                for puzzle in self.classic_mode[act_id]:
                    if puzzle != "name" and "words_found" in self.classic_mode[act_id][puzzle]:
                        for word in self.classic_mode[act_id][puzzle]["words_found"]:
                            if word == word_to_find:
                                nb_words += 1

        elif mode == "legend":

            for act_id in self.legend_mode:
                for puzzle in self.legend_mode[act_id]:
                    if puzzle != "name" and "words_found" in self.legend_mode[act_id][puzzle]:
                        for word in self.legend_mode[act_id][puzzle]["words_found"]:
                            if word == word_to_find:
                                nb_words += 1

        return nb_words

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

# Give extra coins if debug mode
if DEBUG_MODE:
    USER_DATA.user_profile["lincoins"] = 99999
    USER_DATA.user_profile["linclues"] = 200

### Tutorial ###

TUTORIAL = load_json_file(PATH_RESOURCES + "tutorial.json")
GAME_TUTORIAL_DICT = {
    "1": "change_letter",
    "2": "delete_letter",
    "3": "add_letter",
    "4": "practice",
    "5": "reorganize_letters",
    "7": "more_complicated_puzzles"
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
CUSTOMIZATION_LAYOUT_FONT_SIZE = 13
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
POS_HINT_LEFT_TOP_BUTTON = {"x": 0.05, "top": 0.97}
POS_HINT_RIGHT_TOP_BUTTON = {"right": 0.95, "top": 0.97}
POS_HINT_LEFT_BOTTOM_BUTTON = {"x": 0.05, "y": 0.03}
POS_HINT_RIGHT_BOTTOM_BUTTON = {"right": 0.95, "y": 0.03}

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


REWARD_AD = "ca-app-pub-2909842258525517/9568354241"
REWARD_INTERSTITIAL = "ca-app-pub-2909842258525517/1405673632"

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
AMOUNT_UNLIMITED_ADS = [
    {
        "lincoin": 12
    }
]
AMOUNT_WEEKLY_AD = [{
    "lincoin": 480,
    "linclue": 12
}]

### Conversion money ###

DICT_CONVERSION_MONEY = {
    "price_lincoins": 50,
    "reward_linclues": 1
}

### Buy items ###

DICT_AMOUNT_BUY = {
    "1": {
        "reward": 3000,
        "price": 1
    },
    "2": {
        "reward": 50000,
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
GAMEPLAY_LEGEND_DICT = load_json_file(PATH_GAMEPLAY_LEGEND)
QUESTS_DICT = load_json_file(PATH_QUESTS)
CREDITS_DICT = load_json_file(PATH_CREDITS)
ACHIEVEMENTS_DICT = load_json_file(PATH_ACHIEVEMENTS)

### Update the user data if some puzzles have been deleted in the gameplay dict ###

for act_id in USER_DATA.classic_mode:
    for level_id in list(USER_DATA.classic_mode[act_id].keys()):
        if level_id not in GAMEPLAY_DICT[act_id]:
            del USER_DATA.classic_mode[act_id][level_id]
for act_id in USER_DATA.legend_mode:
    for level_id in list(USER_DATA.legend_mode[act_id].keys()):
        if level_id not in GAMEPLAY_LEGEND_DICT[act_id]:
            del USER_DATA.legend_mode[act_id][level_id]
USER_DATA.save_changes()

### Customization with themes and musics ###

CUSTOMIZATION_DICT = load_json_file(PATH_CUSTOMIZATION)
THEMES_DICT = CUSTOMIZATION_DICT["themes"]
MUSICS_DICT = CUSTOMIZATION_DICT["musics"]
THEMES_RARITY_DICT = CUSTOMIZATION_DICT["categories"]
NB_LINCOINS_PER_STAR_CLASSIC_DICT = {
    3: 100,
    2: 70,
    1: 50,
    0: 0
}
NB_LINCOINS_PER_STAR_LEGEND_DICT = {
    3: 200,
    2: 140,
    1: 100,
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


### Max nb of letters in word ###

MAX_NB_LETTERS = 10
