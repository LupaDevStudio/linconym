"""
Module to create the quests screen.
"""

###############
### Imports ###
###############

### Python imports ###

from typing import Literal
from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty
)

### Local imports ###

from tools.constants import (
    SCREEN_TUTORIAL,
    SCREEN_BOTTOM_BAR,
    SCREEN_BACK_ARROW,
    SCREEN_TITLE,
    ACHIEVEMENTS_DICT,
    USER_DATA,
    USER_STATUS_DICT,
    THEMES_DICT,
    GAMEPLAY_DICT
)
from screens.custom_widgets import (
    AchievementsLayout
)
from screens.custom_widgets import (
    LinconymScreen
)


#############
### Class ###
#############


class AchievementsScreen(LinconymScreen):
    """
    Class to manage the screen that contains the achievements.
    """

    dict_type_screen = {
        SCREEN_TITLE: "Achievements",
        SCREEN_BOTTOM_BAR: "none",
        SCREEN_BACK_ARROW: "",
        SCREEN_TUTORIAL: ""
    }
    mode: Literal["classic", "daily"] = StringProperty()

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.fill_scrollview()

    def update_finished_achievements(self, achievement_id: str):
        achievement = ACHIEVEMENTS_DICT[achievement_id]
        series = achievement["series"]

        if series == "status":
            user_status = USER_DATA.user_profile["status"]
            list_user_status_keys = list(USER_STATUS_DICT.keys())
            user_id = list_user_status_keys.index(user_status)
            current_id = list_user_status_keys.index(achievement_id.replace("status_", ""))
            if user_id >= current_id:
                USER_DATA.achievements[achievement_id] = False

        if series == "customization_theme":
            number_themes_to_buy = int(
                achievement_id.replace("customization_theme_", ""))
            number_bought_themes = 0
            for theme in USER_DATA.unlocked_themes:
                if USER_DATA.unlocked_themes[theme]["image"] and theme != "lupa":
                    number_bought_themes += 1
            if number_themes_to_buy <= number_bought_themes:
                USER_DATA.achievements[achievement_id] = False

        if series == "customization_secret_theme":
            number_themes_to_buy = int(
                achievement_id.replace("customization_secret_theme_", ""))
            number_bought_themes = 0
            for theme in USER_DATA.unlocked_themes:
                if USER_DATA.unlocked_themes[theme]["image"]:
                    if THEMES_DICT[theme]["rarity"] == "secret":
                        number_bought_themes += 1
            if number_themes_to_buy <= number_bought_themes:
                USER_DATA.achievements[achievement_id] = False            

        if series == "customization_colors":
            number_themes_to_buy = int(
                achievement_id.replace("customization_colors_", ""))
            number_bought_themes = 0
            for theme in USER_DATA.unlocked_themes:
                if USER_DATA.unlocked_themes[theme]["colors"] and theme != "lupa":
                    number_bought_themes += 1
            if number_themes_to_buy <= number_bought_themes:
                USER_DATA.achievements[achievement_id] = False

        if series == "customization_music":
            number_musics_to_buy = int(
                achievement_id.replace("customization_music_", ""))
            number_bought_musics = len(USER_DATA.unlocked_musics) - 1
            if number_musics_to_buy <= number_bought_musics:
                USER_DATA.achievements[achievement_id] = False

        if series == "cumulated_lincoins":
            number_lincoins_to_cumulate = int(
                achievement_id.replace("cumulated_lincoins_", ""))
            cumulated_lincoins = USER_DATA.user_profile["cumulated_lincoins"]
            if number_lincoins_to_cumulate <= cumulated_lincoins:
                USER_DATA.achievements[achievement_id] = False

        if series == "cumulated_linclues":
            number_linclues_to_cumulate = int(
                achievement_id.replace("cumulated_linclues_", ""))
            cumulated_linclues = USER_DATA.user_profile["cumulated_linclues"]
            if number_linclues_to_cumulate <= cumulated_linclues:
                USER_DATA.achievements[achievement_id] = False

        if series == "cumulated_stars":
            number_stars_to_win = int(
                achievement_id.replace("cumulated_stars_", ""))
            number_stars_won = USER_DATA.get_nb_total_stars()
            if number_stars_to_win <= number_stars_won:
                USER_DATA.achievements[achievement_id] = False

        if series == "acts":
            act_name = achievement_id.replace("acts_", "")
            if act_name in USER_DATA.classic_mode:
                nb_levels = len(GAMEPLAY_DICT[act_name]) - 1
                nb_completed_levels = USER_DATA.get_nb_completed_levels_for_act(
                    act_name)
                if nb_completed_levels == nb_levels:
                    USER_DATA.achievements[achievement_id] = False

        USER_DATA.save_changes()

    def fill_scrollview(self):
        scrollview_layout = self.ids.scrollview_layout

        # Store the widgets
        self.ACHIEVEMENTS_LAYOUT_DICT = {}
        list_achievements_order = []

        for achievement_id in ACHIEVEMENTS_DICT:

            # Check if the achievement has been reached meanwhile
            if not achievement_id in USER_DATA.achievements:
                self.update_finished_achievements(achievement_id)

            achievement = ACHIEVEMENTS_DICT[achievement_id]
            series = achievement["series"]
            reward = achievement["reward"]

            # Get the data of the user
            has_completed = False
            has_got_reward = False
            if achievement_id in USER_DATA.achievements:
                has_completed = True
                if USER_DATA.achievements[achievement_id]:
                    has_got_reward = True

            list_achievements_order.append([
                has_got_reward, not has_completed, series, reward, achievement_id])

        # Sort the list of achievements
        list_achievements_order.sort()

        for tuple_achievement in list_achievements_order:
            achievement_id = tuple_achievement[4]
            reward = tuple_achievement[3]
            series = tuple_achievement[2]
            has_completed = not tuple_achievement[1]
            has_got_reward = tuple_achievement[0]
            achievement = ACHIEVEMENTS_DICT[achievement_id]

            display_condition_series = self.get_display_condition_series(achievement_id)
            display_condition = has_completed or has_got_reward or display_condition_series

            if display_condition:
                current_achievement_layout = AchievementsLayout(
                    achievement_title=achievement["achievement_title"],
                    description=achievement["achievement_content"],
                    reward=reward,
                    font_ratio=self.font_ratio,
                    primary_color=self.primary_color,
                    secondary_color=self.secondary_color,
                    size_hint=(0.8, None),
                    height=150 * self.font_ratio)
                current_achievement_layout.has_completed = has_completed
                current_achievement_layout.has_got_reward = has_got_reward
                current_achievement_layout.release_function = partial(
                    self.get_reward, achievement_id)

                self.ACHIEVEMENTS_LAYOUT_DICT[achievement_id] = current_achievement_layout
                scrollview_layout.add_widget(current_achievement_layout)

    def get_display_condition_series(self, achievement_id):
        achievement = ACHIEVEMENTS_DICT[achievement_id]
        series = achievement["series"]
        number_series = achievement["number_series"]
        series_achievements = []

        for id in USER_DATA.achievements:
            if series in id:
                series_achievements.append(ACHIEVEMENTS_DICT[id]["number_series"])

        user_in_series = max(series_achievements) if series_achievements != [] else 0

        # Display only the acts unlocked
        if series == "acts":
            act_name = achievement_id.replace("acts_", "")
            return act_name in USER_DATA.classic_mode

        # Display only the next achievement for most series
        else:
            return user_in_series + 1 == number_series

    def get_reward(self, achievement_id):
        achievement = ACHIEVEMENTS_DICT[achievement_id]
        reward = achievement["reward"]
        USER_DATA.achievements[achievement_id] = True
        USER_DATA.user_profile["lincoins"] += reward
        USER_DATA.user_profile["cumulated_lincoins"] += reward
        USER_DATA.save_changes()

        # Rebuild scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
