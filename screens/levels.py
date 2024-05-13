"""
Module to create the levels screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty
)

### Local imports ###

from tools.constants import (
    SCREEN_BACK_ARROW,
    SCREEN_BOTTOM_BAR,
    SCREEN_TUTORIAL
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

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current_act_id: str

    def reload_kwargs(self, dict_kwargs):
        self.current_act_id = dict_kwargs["current_act_id"]

    def on_pre_enter(self, *args):
        self.ids.level_layout.act_id = self.current_act_id
        self.ids.level_layout.build_layout()
        self.current_act_name = "Act " + self.current_act_id
        return super().on_pre_enter(*args)

    def on_leave(self, *args):
        self.ids.level_layout.clear_widgets()
        return super().on_leave(*args)

    def go_to_quests_screen(self):
        current_dict_kwargs = {
            "current_act_id": self.current_act_id
        }
        next_dict_kwargs = {
            "current_act_id": self.current_act_id,
            "current_level_id": None
        }
        self.manager.go_to_next_screen(
            next_screen_name="quests",
            current_dict_kwargs=current_dict_kwargs,
            next_dict_kwargs=next_dict_kwargs
        )

    def open_game_screen(self, level_id):
        current_dict_kwargs = {
            "current_act_id": self.current_act_id
        }
        next_dict_kwargs = {
            "current_act_id": self.current_act_id,
            "current_level_id": level_id
        }
        self.manager.go_to_next_screen(
            next_screen_name="game",
            current_dict_kwargs=current_dict_kwargs,
            next_dict_kwargs=next_dict_kwargs
        )
