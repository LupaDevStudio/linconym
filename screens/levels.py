"""
Module to create the levels screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty
)

### Local imports ###

from tools.constants import (
    SCREEN_BACK_ARROW,
    SCREEN_BOTTOM_BAR,
    SCREEN_TUTORIAL,
    USER_DATA
)
from screens.custom_widgets import (
    LinconymScreen
)
from tools import (
    music_mixer
)


#############
### Class ###
#############


class LevelsScreen(LinconymScreen):
    """
    Class to manage the levels screen which allow the user to select a level inside an act.
    """

    dict_type_screen = {
        SCREEN_BOTTOM_BAR: "none",
        SCREEN_BACK_ARROW: "",
        SCREEN_TUTORIAL: ""
    }
    current_act_name = StringProperty()
    mode = StringProperty()
    nb_stars = NumericProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current_act_id: str

    def reload_kwargs(self, dict_kwargs):
        self.current_act_id = dict_kwargs["current_act_id"]
        self.mode = dict_kwargs["mode"]
        self.nb_stars = USER_DATA.get_mean_nb_stars_on_act(self.current_act_id, mode=self.mode)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.ids.level_layout.act_id = self.current_act_id
        self.ids.level_layout.mode = self.mode
        self.ids.level_layout.build_layout()
        if self.mode == "legend":
            self.current_act_name = "Legend "
        else:
            self.current_act_name = ""
        self.current_act_name += "Act " + self.current_act_id

    def on_pre_leave(self, *args):
        # Take screenshot for adv
        # self.export_to_png("test.png", scale=2.732)

        return super().on_pre_leave(*args)

    def on_leave(self, *args):
        self.ids.level_layout.clear_widgets()
        return super().on_leave(*args)

    def go_to_quests_screen(self):
        current_dict_kwargs = {
            "current_act_id": self.current_act_id,
            "mode": self.mode
        }
        next_dict_kwargs = {
            "current_act_id": self.current_act_id,
            "current_level_id": None,
            "mode": self.mode
        }
        self.manager.go_to_next_screen(
            next_screen_name="quests",
            current_dict_kwargs=current_dict_kwargs,
            next_dict_kwargs=next_dict_kwargs
        )

    def open_game_screen(self, level_id):
        current_dict_kwargs = {
            "current_act_id": self.current_act_id,
            "mode": self.mode
        }
        next_dict_kwargs = {
            "current_act_id": self.current_act_id,
            "current_level_id": level_id,
            "mode": self.mode
        }
        self.manager.go_to_next_screen(
            next_screen_name="game",
            current_dict_kwargs=current_dict_kwargs,
            next_dict_kwargs=next_dict_kwargs
        )
