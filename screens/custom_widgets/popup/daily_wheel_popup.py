"""
Module to create a popup to allow the user to regenerate lives.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty,
    ObjectProperty
)
from kivy.animation import Animation, AnimationTransition

### Local imports ###

from screens.custom_widgets.popup.custom_popup import CustomPopup
from tools.constants import (
    USER_DATA
)
from tools import sound_mixer

#################
### Constants ###
#################

ANGLE_PORTION = 360 / 16
SMALL_REWARD_LINCOINS = {
    "lincoin": 50
}
SMALL_REWARD_LINCLUES = {
    "linclue": 1
}
MEDIUM_REWARD_LINCOINS = {
    "lincoin": 100
}
MEDIUM_REWARD_LINCLUES = {
    "linclue": 2
}
BIG_REWARD = {
    "linclue": 3,
    "lincoin": 500
}
DAILY_WHEEL_DICT = {
    0: SMALL_REWARD_LINCOINS,
    1: MEDIUM_REWARD_LINCLUES,
    2: SMALL_REWARD_LINCOINS,
    3: SMALL_REWARD_LINCLUES,
    4: BIG_REWARD,
    5: SMALL_REWARD_LINCOINS,
    6: MEDIUM_REWARD_LINCLUES,
    7: SMALL_REWARD_LINCOINS,
    8: SMALL_REWARD_LINCLUES,
    9: MEDIUM_REWARD_LINCOINS,
    10: SMALL_REWARD_LINCLUES,
    11: SMALL_REWARD_LINCOINS,
    12: BIG_REWARD,
    13: SMALL_REWARD_LINCLUES,
    14: MEDIUM_REWARD_LINCOINS,
    15: SMALL_REWARD_LINCLUES
}

#############
### Class ###
#############


class DailyWheelPopup(CustomPopup):

    title = StringProperty()
    angle = NumericProperty(0)
    primary_color = ColorProperty()
    secondary_color = ColorProperty()
    color_label_button = ColorProperty((1, 1, 1, 1))
    release_function = ObjectProperty(lambda: 1 + 1)
    button_label = StringProperty()

    last_angle: int
    reward_linclues = NumericProperty(0)
    reward_lincoins = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Daily Wheel"
        self.previous_portion = None

    def on_open(self):
        self.release_function = self.start_animation
        self.button_label = "Spin"
        self.reward_linclues = 0
        self.reward_lincoins = 0
        return super().on_open()

    def on_angle(self, item, angle):
        portion = int(angle / ANGLE_PORTION)
        if portion != self.previous_portion:
            sound_mixer.change_volume(0.5, "spin_tick")
            self.previous_portion = portion
            print("tick")
        if angle == 360:
            item.angle = 0

    def start_animation(self):
        number_of_turns = rd.randint(4, 7)
        self.last_angle = rd.randint(0, 360)
        total_angle = self.last_angle + 360 * number_of_turns
        anim = Animation(angle=total_angle, duration=number_of_turns,
                         t=AnimationTransition.out_quad)
        anim.start(self)
        self.ids.button.disabled = True
        anim.on_complete = self.finish_animation

    def finish_animation(self, *args):
        self.button_label = "Close"
        self.ids.button.disabled = False
        self.release_function = self.dismiss

        # Compute the rewards
        portion = int(self.last_angle / ANGLE_PORTION)
        reward_dict = DAILY_WHEEL_DICT[portion]
        if "linclue" in reward_dict:
            self.reward_linclues = reward_dict["linclue"]
            USER_DATA.user_profile["linclues"] += self.reward_linclues
            USER_DATA.user_profile["cumulated_linclues"] += self.reward_linclues
        if "lincoin" in reward_dict:
            self.reward_lincoins = reward_dict["lincoin"]
            USER_DATA.user_profile["lincoins"] += self.reward_lincoins
            USER_DATA.user_profile["cumulated_lincoins"] += self.reward_lincoins
