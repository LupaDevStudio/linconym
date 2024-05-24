"""
Module to create the act button.
"""

###############
### Imports ###
###############

from functools import partial

### Kivy imports ###

from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    ColorProperty
)

### Local imports ###

from tools.path import (
    PATH_TITLE_FONT
)
from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    CONTENT_LABEL_FONT_SIZE
)
from screens.custom_widgets import (
    RoundButton
)
from screens.custom_widgets.layout.money_layout import MoneyLayout

#############
### Class ###
#############


class BoosterLayout(RelativeLayout):
    """
    A layout to display the boosters.
    """

    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    mode = StringProperty()  # can be "ads" or "buy" or "conversion"
    booster_title = StringProperty()
    font_size = NumericProperty(CONTENT_LABEL_FONT_SIZE)
    font_ratio = NumericProperty(1)
    text_font_name = StringProperty(PATH_TITLE_FONT)

    list_widgets = []
    list_infos = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(list_infos=self.build_layout)

    def clear_layout(self):
        for widget in self.list_widgets:
            self.remove_widget(widget)
        self.list_widgets = []

    def build_layout(self, base_widget, value):
        self.clear_layout()

        number_circles = len(self.list_infos)
        list_positions_x = []
        for i in range(1, number_circles + 1):
            position = i/(number_circles + 1)
            if position == 0.25:
                position = 0.2
            elif position == 0.75:
                position = 0.8
            list_positions_x.append(position)
        for counter in range(len(self.list_infos)):

            text = str(self.list_infos[counter]["price"]) if "price" in self.list_infos[counter] else ""

            icon_mode = False
            if "price_unit" in self.list_infos[counter]:
                if self.list_infos[counter]["price_unit"] not in ["lincoin", "linclue"]:
                    text += self.list_infos[counter]["price_unit"]
                else:
                    icon_mode = True
                    text = ""

            disable_button = False
            if "disable_button" in self.list_infos[counter]:
                disable_button = self.list_infos[counter]["disable_button"]
            
            round_button = RoundButton(
                pos_hint={"center_x": list_positions_x[counter], "center_y": 0.5},
                size_hint=(None, 0.4),
                color=self.list_infos[counter]["circle_color"],
                line_width=2,
                text=text,
                font_ratio=self.font_ratio,
                release_function=self.list_infos[counter]["release_function"],
                disable_button=disable_button
            )
            round_button.bind(height=round_button.setter("width"))
            self.list_widgets.append(round_button)
            self.add_widget(round_button)

            if icon_mode:
                money_layout = MoneyLayout(
                    coins_count=self.list_infos[counter]["price"],
                    font_ratio=self.font_ratio,
                    size_hint=(None, 0.25),
                    font_size=self.font_size,
                    pos_hint={"center_x": list_positions_x[counter], "center_y": 0.5}
                )
                self.add_widget(money_layout)

            # Money
            relative_layout = RelativeLayout(
                size_hint=(1, 0.3),
                pos_hint={"center_x":0.5, "y":0}
            )

            list_rewards = self.list_infos[counter]["reward"]
            number_rewards = len(list_rewards)

            list_positions_rewards_x = []
            for counter_reward in range(1, number_rewards + 1):
                temp_list = []
                central_position = counter_reward / (number_rewards + 1)
                if central_position == 0.25:
                    central_position = 0.2
                elif central_position == 0.75:
                    central_position = 0.8

                number_units = len(list_rewards[counter_reward-1])

                if list_positions_x[counter] != 0.5:
                    central_position = list_positions_x[counter]

                if number_units == 1:
                    temp_list.append(central_position)
                elif number_units == 2:
                    temp_list.append(central_position - (1/(number_rewards+1.4))/2)
                    temp_list.append(central_position + (1/(number_rewards+1.4))/2)
                
                list_positions_rewards_x.append(temp_list)

            for counter_reward in range(number_rewards):
                dict_reward = list_rewards[counter_reward]
                number_units = len(dict_reward)

                for counter_unit in range(number_units):
                    unit = list(dict_reward.keys())[counter_unit]
                    amount = dict_reward[unit]

                    money_layout = MoneyLayout(
                        coins_count=amount,
                        and_mode=True if counter_unit > 0 else False,
                        or_mode=True if counter_reward > 0 else False,
                        unit=unit,
                        font_ratio=self.font_ratio,
                        size_hint=(1/number_rewards, 1),
                        font_size=self.font_size,
                        pos_hint={"center_x":list_positions_rewards_x[counter_reward][counter_unit], "y":0}
                    )
                    relative_layout.add_widget(money_layout)

            self.list_widgets.append(relative_layout)
            self.add_widget(relative_layout)
