"""
Module to create the quests screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty
)

### Local imports ###

from tools.constants import (
    SCREEN_TUTORIAL,
    USER_DATA,
    GAMEPLAY_DICT,
    GAMEPLAY_LEGEND_DICT
)
from screens.custom_widgets import (
    LinconymScreen
)


#############
### Class ###
#############


class ConfigureTreeScreen(LinconymScreen):
    """
    Class to manage the screen that contains the profile information.
    """

    current_level_name = StringProperty()
    dict_type_screen = {
        SCREEN_TUTORIAL: ""
    }
    nb_stars = NumericProperty()
    start_word = StringProperty("BOY")
    end_word = StringProperty("TOYS")
    hide_completed_branches = BooleanProperty(False)
    mode = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current_act_id: str
        self.current_level_id: str | None

    def reload_kwargs(self, dict_kwargs):
        self.current_act_id = dict_kwargs["current_act_id"]
        self.current_level_id = dict_kwargs["current_level_id"]
        self.mode = dict_kwargs["mode"]

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        if self.mode == "classic":

            # Extract info from user data
            self.nb_stars = USER_DATA.classic_mode[self.current_act_id][self.current_level_id]["nb_stars"]
            position_to_word_id = USER_DATA.classic_mode[self.current_act_id][
                self.current_level_id]["position_to_word_id"].copy()
            current_position = USER_DATA.classic_mode[self.current_act_id][
                self.current_level_id]["current_position"]
            words_found = USER_DATA.classic_mode[self.current_act_id][self.current_level_id]["words_found"]
            self.start_word = GAMEPLAY_DICT[self.current_act_id][self.current_level_id]["start_word"].upper(
            )
            self.end_word = GAMEPLAY_DICT[self.current_act_id][self.current_level_id]["end_word"].upper(
            )

        elif self.mode == "legend":

            # Extract info from user data
            self.nb_stars = USER_DATA.legend_mode[self.current_act_id][self.current_level_id]["nb_stars"]
            position_to_word_id = USER_DATA.legend_mode[self.current_act_id][
                self.current_level_id]["position_to_word_id"].copy()
            current_position = USER_DATA.legend_mode[self.current_act_id][
                self.current_level_id]["current_position"]
            words_found = USER_DATA.legend_mode[self.current_act_id][self.current_level_id]["words_found"]
            self.start_word = GAMEPLAY_LEGEND_DICT[self.current_act_id][self.current_level_id]["start_word"].upper()
            self.end_word = GAMEPLAY_LEGEND_DICT[self.current_act_id][self.current_level_id]["end_word"].upper()
        
        self.hide_completed_branches = USER_DATA.settings["hide_completed_branches"]

        self.ids["tree_layout"].build_layout(
            position_to_word_id=position_to_word_id.copy(),
            words_found=words_found,
            current_position=current_position,
            end_word=self.end_word.lower()
        )

        # Create the title of the screen
        temp = self.current_act_id.replace("Act", "")
        self.current_level_name = "Act " + temp + " – " + self.current_level_id

    def display_hide_path(self):
        if self.hide_completed_branches:
            self.hide_completed_branches = False
            self.ids.tree_layout.show_completed_branches()
        else:
            self.hide_completed_branches = True
            self.ids.tree_layout.mask_completed_branches()
        USER_DATA.settings["hide_completed_branches"] = self.hide_completed_branches
        if self.mode == "classic":
            USER_DATA.classic_mode[self.current_act_id][self.current_level_id][
                "current_position"] = self.ids["tree_layout"].current_position
        elif self.mode == "legend":
            USER_DATA.classic_mode[self.current_act_id][self.current_level_id][
                "current_position"] = self.ids["tree_layout"].current_position
        USER_DATA.save_changes()

    def open_game(self):
        """
        Open the game screen.
        """
        self.manager.go_to_previous_screen()

    def on_change_word_position_on_tree(self):
        # Save the new current position
        if self.mode == "classic":
            USER_DATA.classic_mode[self.current_act_id][self.current_level_id][
                "current_position"] = self.ids["tree_layout"].current_position
        elif self.mode == "legend":
            USER_DATA.legend_mode[self.current_act_id][self.current_level_id][
                "current_position"] = self.ids["tree_layout"].current_position
        USER_DATA.save_changes()

    def open_levels_screen(self):
        # Open the screen
        next_dict_kwargs = {
            "current_act_id": self.current_act_id,
            "mode": self.mode
        }
        current_dict_kwargs = {
            "current_act_id": self.current_act_id,
            "current_level_id": self.current_level_id,
            "mode": self.mode
        }
        self.go_to_next_screen(
            screen_name="levels",
            next_dict_kwargs=next_dict_kwargs,
            current_dict_kwargs=current_dict_kwargs)
