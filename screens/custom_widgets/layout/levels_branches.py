"""
Module to create the levels tree for the levels screen.
"""

###############
### Imports ###
###############

### Python imports ###

from math import ceil

### Kivy imports ###

from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    NumericProperty,
    BooleanProperty,
    ColorProperty,
    StringProperty,
    ListProperty
)

### Local imports ###

from tools.kivy_tools.tools_kivy import MyScrollViewLayout

from tools.constants import (
    USER_DATA,
    GAMEPLAY_DICT,
    OPACITY_ON_BUTTON_PRESS,
    MAX_NB_LEVELS_PER_BRANCH,
    LEVEL_BUTTON_SIZE_HINT,
    LEVEL_BUTTON_SPACING,
    LEVEL_BUTTON_SIDE_OFFSET,
    LEVEL_BUTTON_RELATIVE_HEIGHT
)


###############
### Classes ###
###############


class StraightBranch(Widget):
    color = ColorProperty()
    font_ratio = NumericProperty(1)


class CurveBranchTopLeft(Widget):
    color = ColorProperty()
    font_ratio = NumericProperty(1)


class CurveBranchTopRight(Widget):
    color = ColorProperty()
    font_ratio = NumericProperty(1)


class CurveBranchBottomRight(Widget):
    color = ColorProperty()
    font_ratio = NumericProperty(1)


class CurveBranchBottomLeft(Widget):
    color = ColorProperty()
    font_ratio = NumericProperty(1)


class LevelButton(ButtonBehavior, RelativeLayout):

    nb_stars = NumericProperty()
    font_ratio = NumericProperty(1)
    level_label_text = StringProperty()
    primary_color = ColorProperty((0.5, 0.5, 0.5, 1))
    secondary_color = ColorProperty((0.2, 0.2, 0.2, 1))
    is_unlocked = BooleanProperty(False)
    disable_button = BooleanProperty(False)

    def __init__(
            self,
            level_id=0,
            is_unlocked=False,
            nb_stars=0,
            **kw):
        super().__init__(**kw)
        self.always_release = True
        self.is_unlocked = is_unlocked
        self.level_id = level_id
        self.level_label_text = str(level_id)
        self.nb_stars = nb_stars
        self.bind(is_unlocked=self.update_status)
        self.update_status()

    def update_status(self, value=None, base_widget=None):
        self.disable_button = not (self.is_unlocked)

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            self.opacity = 1
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.get_root_window().children[0].get_screen(
                    "levels").open_game_screen(str(self.level_id))


class LevelBranch(RelativeLayout):

    font_ratio = NumericProperty(1)
    primary_color = ColorProperty((0.5, 0.5, 0.5, 1))
    secondary_color = ColorProperty((0.2, 0.2, 0.2, 1))

    def __init__(
            self,
            act_id="1",
            branch_id=0,
            **kw):
        super().__init__(**kw)
        self.act_id = act_id
        self.branch_id = branch_id
        self.build_layout()

    def compute_level_button_pos_hint(self, local_id: int):
        """
        Compute the pos hint of a level button given its local id.

        Parameters
        ----------
        local_id : int
            Local id of the level button inside the level branch.

        Returns
        -------
        dict
            Position hint dictionnary for the level button.
        """
        pos_hint = {}
        if self.branch_id % 2 == 0:
            center_x = LEVEL_BUTTON_SIDE_OFFSET + (LEVEL_BUTTON_SIZE_HINT + LEVEL_BUTTON_SPACING) * \
                local_id + LEVEL_BUTTON_SIZE_HINT / 2
            if local_id + 1 < MAX_NB_LEVELS_PER_BRANCH:
                pos_hint["top"] = 1
            else:
                pos_hint["y"] = (1 - LEVEL_BUTTON_RELATIVE_HEIGHT * 2) / 2
                center_x = center_x - LEVEL_BUTTON_SPACING
        else:
            center_x = 1 - (LEVEL_BUTTON_SIDE_OFFSET + (LEVEL_BUTTON_SIZE_HINT + LEVEL_BUTTON_SPACING) *
                            local_id + LEVEL_BUTTON_SIZE_HINT / 2)
            if local_id + 1 < MAX_NB_LEVELS_PER_BRANCH:
                pos_hint["top"] = 1
            else:
                pos_hint["y"] = (1 - LEVEL_BUTTON_RELATIVE_HEIGHT * 2) / 2
                center_x = center_x + LEVEL_BUTTON_SPACING
        pos_hint["center_x"] = center_x
        return pos_hint

    def build_layout(self):
        """
        Add all buttons to the layout to build the branch.
        """
        # Find the number of levels contained in the branch, cannot be greater than MAX_NB_LEVELS_PER_BRANCH
        nb_levels = len(GAMEPLAY_DICT[self.act_id]) - 1
        self.local_nb_levels = min(
            nb_levels - self.branch_id * MAX_NB_LEVELS_PER_BRANCH, 4)
        # Add the first branch to link with the previous line
        if self.branch_id > 0:
            previous_level_is_unlocked = str(self.branch_id * MAX_NB_LEVELS_PER_BRANCH) \
                in USER_DATA.classic_mode[self.act_id]
            if previous_level_is_unlocked:
                branch_color = self.primary_color
            else:
                branch_color = self.secondary_color
            if self.branch_id % 2 == 1:

                branch_pos_hint = {
                    "x": 1 - LEVEL_BUTTON_SIDE_OFFSET,
                    "top": 1 + (1 - LEVEL_BUTTON_RELATIVE_HEIGHT * 2) / 2}
                branch_size_hint = (
                    LEVEL_BUTTON_SPACING + LEVEL_BUTTON_SIZE_HINT / 2, LEVEL_BUTTON_RELATIVE_HEIGHT / 2 + (1 - 2 * LEVEL_BUTTON_RELATIVE_HEIGHT) / 2)
                branch = CurveBranchBottomLeft(
                    size_hint=branch_size_hint,
                    pos_hint=branch_pos_hint,
                    color=branch_color,
                    font_ratio=self.font_ratio
                )
            else:
                branch_pos_hint = {
                    "x": LEVEL_BUTTON_SIZE_HINT / 2,
                    "top": 1 + (1 - LEVEL_BUTTON_RELATIVE_HEIGHT * 2) / 2}
                branch_size_hint = (
                    LEVEL_BUTTON_SPACING + LEVEL_BUTTON_SIZE_HINT / 2, LEVEL_BUTTON_RELATIVE_HEIGHT / 2 + (1 - 2 * LEVEL_BUTTON_RELATIVE_HEIGHT) / 2)
                branch = CurveBranchBottomRight(
                    size_hint=branch_size_hint,
                    pos_hint=branch_pos_hint,
                    color=branch_color,
                    font_ratio=self.font_ratio
                )
            self.add_widget(branch)
        for local_id in range(self.local_nb_levels):
            # Create the level button
            level_id = local_id + 1 + self.branch_id * MAX_NB_LEVELS_PER_BRANCH
            level_key = str(level_id)
            level_pos_hint = self.compute_level_button_pos_hint(local_id)
            if level_key in USER_DATA.classic_mode[self.act_id]:
                level_is_unlocked = True
                level_nb_stars = USER_DATA.classic_mode[self.act_id][level_key]["nb_stars"]
            else:
                level_is_unlocked = False
                level_nb_stars = 0
            level_button = LevelButton(level_id=level_id,
                                       is_unlocked=level_is_unlocked,
                                       nb_stars=level_nb_stars,
                                       pos_hint=level_pos_hint,
                                       size_hint=(
                                           LEVEL_BUTTON_SIZE_HINT, LEVEL_BUTTON_RELATIVE_HEIGHT),
                                       primary_color=self.primary_color,
                                       secondary_color=self.secondary_color,
                                       font_ratio=self.font_ratio)
            self.add_widget(level_button)
            # Create the branch
            if level_id < nb_levels:

                if level_is_unlocked:
                    branch_color = self.primary_color
                else:
                    branch_color = self.secondary_color
                if self.branch_id % 2 == 0:
                    if local_id + 2 < MAX_NB_LEVELS_PER_BRANCH:
                        branch_size_hint = (
                            LEVEL_BUTTON_SPACING, LEVEL_BUTTON_RELATIVE_HEIGHT)
                        branch_pos_hint = {
                            "center_x": level_pos_hint["center_x"] + LEVEL_BUTTON_SPACING / 2 + LEVEL_BUTTON_SIZE_HINT / 2}
                        branch_pos_hint["top"] = level_pos_hint["top"]
                        branch = StraightBranch(
                            size_hint=branch_size_hint,
                            pos_hint=branch_pos_hint,
                            color=branch_color,
                            font_ratio=self.font_ratio
                        )
                    elif local_id + 2 == MAX_NB_LEVELS_PER_BRANCH:
                        branch_pos_hint = {
                            "x": level_pos_hint["center_x"] + LEVEL_BUTTON_SIZE_HINT / 2,
                            "top": level_pos_hint["top"] - LEVEL_BUTTON_RELATIVE_HEIGHT / 2}
                        branch_size_hint = (
                            LEVEL_BUTTON_SPACING + LEVEL_BUTTON_SIZE_HINT / 2, LEVEL_BUTTON_RELATIVE_HEIGHT / 2 + (1 - 2 * LEVEL_BUTTON_RELATIVE_HEIGHT) / 2)
                        branch = CurveBranchTopLeft(
                            size_hint=branch_size_hint,
                            pos_hint=branch_pos_hint,
                            color=branch_color,
                            font_ratio=self.font_ratio
                        )
                    else:
                        continue
                    self.add_widget(branch)
                else:
                    if local_id + 2 < MAX_NB_LEVELS_PER_BRANCH:
                        branch_size_hint = (
                            LEVEL_BUTTON_SPACING, LEVEL_BUTTON_RELATIVE_HEIGHT)
                        branch_pos_hint = {
                            "center_x": level_pos_hint["center_x"] - LEVEL_BUTTON_SPACING / 2 - LEVEL_BUTTON_SIZE_HINT / 2}
                        branch_pos_hint["top"] = level_pos_hint["top"]
                        branch = StraightBranch(
                            size_hint=branch_size_hint,
                            pos_hint=branch_pos_hint,
                            color=branch_color,
                            font_ratio=self.font_ratio
                        )
                    elif local_id + 2 == MAX_NB_LEVELS_PER_BRANCH:
                        branch_pos_hint = {
                            "right": level_pos_hint["center_x"] - LEVEL_BUTTON_SIZE_HINT / 2,
                            "top": level_pos_hint["top"] - LEVEL_BUTTON_RELATIVE_HEIGHT / 2}
                        branch_size_hint = (
                            LEVEL_BUTTON_SPACING + LEVEL_BUTTON_SIZE_HINT / 2, LEVEL_BUTTON_RELATIVE_HEIGHT / 2 + (1 - 2 * LEVEL_BUTTON_RELATIVE_HEIGHT) / 2)
                        branch = CurveBranchTopRight(
                            size_hint=branch_size_hint,
                            pos_hint=branch_pos_hint,
                            color=branch_color,
                            font_ratio=self.font_ratio
                        )
                    else:
                        continue
                    self.add_widget(branch)


class LevelLayout(MyScrollViewLayout):

    font_ratio = NumericProperty()
    primary_color = ColorProperty((0.5, 0.5, 0.5, 1))
    secondary_color = ColorProperty((0.2, 0.2, 0.2, 1))
    nb_branches = NumericProperty()
    font_ratio = NumericProperty(1)

    def __init__(
            self,
            act_id="1",
            **kw):
        super().__init__(**kw)
        self.act_id = act_id
        self.cols = 1
        self.spacing = 0

    def build_layout(self):
        nb_levels = len(GAMEPLAY_DICT[self.act_id]) - 1
        self.nb_branches = ceil(nb_levels / MAX_NB_LEVELS_PER_BRANCH)
        for branch_id in range(self.nb_branches):
            level_branch = LevelBranch(
                act_id=self.act_id,
                branch_id=branch_id,
                primary_color=self.primary_color,
                secondary_color=self.secondary_color,
                font_ratio=self.font_ratio)
            self.add_widget(level_branch)
