"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Local imports ###

from tools.constants import (
    USER_DATA,
    SCREEN_TUTORIAL,
    GAMEPLAY_DICT,
    SCREEN_TITLE,
    SCREEN_BOTTOM_BAR
)
from screens.custom_widgets import (
    LinconymScreen
)
from screens.custom_widgets import (
    ActButton
)

#############
### Class ###
#############


class ClassicModeScreen(LinconymScreen):

    dict_type_screen = {
        SCREEN_TITLE: "Classic Mode",
        SCREEN_BOTTOM_BAR: "none",
        SCREEN_TUTORIAL: ""
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.ACT_BUTTON_DICT = {}
        self.on_resize()
        self.fill_scrollview()

    def on_pre_enter(self, *args):
        # Recover the total nb of stars of the user
        nb_total_stars = USER_DATA.get_nb_total_stars()

        # Update the info on the act buttons
        for act in self.ACT_BUTTON_DICT:
            current_act_button: ActButton = self.ACT_BUTTON_DICT[act]
            current_act_button.primary_color = self.primary_color
            current_act_button.secondary_color = self.secondary_color
            current_act_button.nb_total_stars = nb_total_stars
            mean_nb_stars = USER_DATA.get_mean_nb_stars_on_act(act)
            current_act_button.nb_stars = mean_nb_stars
            if act in USER_DATA.classic_mode:
                nb_completed_levels = USER_DATA.get_nb_completed_levels_for_act(
                    act)
                current_act_button.nb_completed_levels = nb_completed_levels
            nb_stars_to_unlock = 20 * (int(act) - 1)
            if nb_total_stars < nb_stars_to_unlock:
                disable_act_button = True
            else:
                disable_act_button = False
            current_act_button.disabled = disable_act_button

        return super().on_pre_enter(*args)

    def on_resize(self, *args):
        for act in self.ACT_BUTTON_DICT:
            self.ACT_BUTTON_DICT[act].font_ratio = self.font_ratio
        return super().on_resize(*args)

    def fill_scrollview(self):

        # Recover the total nb of stars
        nb_total_stars = USER_DATA.get_nb_total_stars()

        scrollview_layout = self.ids["scrollview_layout"]
        # Load the widgets
        self.ACT_BUTTON_DICT = {}
        for act in GAMEPLAY_DICT:

            # Extract the act informationg
            act_title = GAMEPLAY_DICT[act]["name"]
            nb_levels = len(GAMEPLAY_DICT[act]) - 1
            nb_stars_to_unlock = 20 * (int(act) - 1)
            if act in USER_DATA.classic_mode:
                nb_completed_levels = USER_DATA.get_nb_completed_levels_for_act(
                    act)
            else:
                nb_completed_levels = 0
                disable_act_button = True
            if nb_total_stars < nb_stars_to_unlock:
                disable_act_button = True
            else:
                disable_act_button = False
            mean_nb_stars = USER_DATA.get_mean_nb_stars_on_act(act)

            # Create the act button
            current_act_button = ActButton(
                act_title=act_title,
                nb_levels=nb_levels,
                nb_completed_levels=nb_completed_levels,
                nb_stars=mean_nb_stars,
                font_ratio=self.font_ratio,
                release_function=partial(self.open_levels_screen, act),
                primary_color=self.primary_color,
                secondary_color=self.secondary_color,
                nb_stars_to_unlock=nb_stars_to_unlock,
                nb_total_stars=nb_total_stars,
                disabled=disable_act_button)
            self.ACT_BUTTON_DICT[act] = current_act_button
            scrollview_layout.add_widget(self.ACT_BUTTON_DICT[act])

    def open_levels_screen(self, act_id):
        # Create data if it is the first time that the play opens the act
        if act_id not in USER_DATA.classic_mode:
            USER_DATA.classic_mode[act_id] = {"1": {"nb_stars": 0}}
            USER_DATA.save_changes()

        # Open the screen
        dict_kwargs = {
            "current_act_id": act_id
        }
        self.manager.go_to_next_screen(
            next_screen_name="levels",
            next_dict_kwargs=dict_kwargs)
