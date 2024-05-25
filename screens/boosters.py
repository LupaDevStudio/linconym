"""
Module to create the profile screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial
from typing import Literal

### Kivy imports ###

from kivy.properties import (
    NumericProperty,
    ListProperty
)

### Local imports ###

from tools.constants import (
    USER_DATA,
    SCREEN_TUTORIAL,
    AMOUNT_DAILY_ADS,
    AMOUNT_WEEKLY_AD,
    DICT_CONVERSION_MONEY,
    DICT_AMOUNT_BUY,
    SCREEN_BACK_ARROW,
    SCREEN_BOTTOM_BAR,
    SCREEN_TITLE
)
from screens.custom_widgets import (
    LinconymScreen,
    MessagePopup
)


#############
### Class ###
#############


class BoostersScreen(LinconymScreen):
    """
    Class to manage the screen with the coins boosters.
    """

    dict_type_screen = {
        SCREEN_TITLE: "Boosters",
        SCREEN_BOTTOM_BAR: "none",
        SCREEN_BACK_ARROW: "",
        SCREEN_TUTORIAL: ""
    }

    lincoins_count = NumericProperty()
    linclues_count = NumericProperty()
    list_daily_ads = ListProperty()
    list_weekly_ads = ListProperty()
    list_conversion = ListProperty()
    list_buy = ListProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.update_all_widgets()

    def on_enter(self, *args):
        super().on_enter(*args)

    def update_all_widgets(self):
        self.lincoins_count = USER_DATA.user_profile["lincoins"]
        self.linclues_count = USER_DATA.user_profile["linclues"]
        self.build_list_daily_ads()
        self.build_list_weekly_ads()
        self.build_list_conversion()
        self.build_list_buy()

    def build_list_daily_ads(self):
        self.list_daily_ads = []
        enable_button = USER_DATA.ads["number_daily_ads_left"] > 0
        circle_color = self.primary_color if enable_button else self.secondary_color

        self.list_daily_ads.append({
            "price": str(USER_DATA.ads["number_daily_ads_left"]),
            "reward": AMOUNT_DAILY_ADS,
            "circle_color": circle_color,
            "disable_button": not enable_button,
            "release_function": partial(self.see_ad, "daily")
        })

    def build_list_weekly_ads(self):
        self.list_weekly_ads = []
        enable_button = USER_DATA.ads["number_weekly_ads_left"] > 0
        circle_color = self.primary_color if enable_button else self.secondary_color

        self.list_weekly_ads.append({
            "price": str(USER_DATA.ads["number_weekly_ads_left"]),
            "reward": AMOUNT_WEEKLY_AD,
            "circle_color": circle_color,
            "disable_button": not enable_button,
            "release_function": partial(self.see_ad, "weekly")
        })

    def build_list_conversion(self):
        self.list_conversion = []

        # If the user has enough money to perform the conversion
        enable_button = self.lincoins_count >= DICT_CONVERSION_MONEY["price_lincoins"]
        circle_color = self.primary_color if enable_button else self.secondary_color

        self.list_conversion.append({
            "circle_color": circle_color,
            "reward": [{"linclue": DICT_CONVERSION_MONEY["reward_linclues"]}],
            "price": DICT_CONVERSION_MONEY["price_lincoins"],
            "price_unit": "lincoin",
            "disable_button": not enable_button,
            "release_function": self.convert_lincoin_to_linclue
        })

    def build_list_buy(self):
        temp_list = []
        self.list_buy = []
        for counter in range(1, 4):
            temp_list.append({
                "circle_color": self.primary_color,
                "reward": [{"lincoin": DICT_AMOUNT_BUY[str(counter)]["reward"]}],
                "price_unit": "€",
                "price": DICT_AMOUNT_BUY[str(counter)]["price"],
                "release_function": partial(self.buy_booster, counter)
            })
        self.list_buy = temp_list

    def see_ad(self, mode: Literal["daily", "weekly"]):
        """
        Launch the ad and update the display.

        Parameters
        ----------
        mode : Literal["daily", "weekly"]
            Mode according to which it is a daily or weekly ad.

        Returns
        -------
        None
        """
        USER_DATA.change_boosters(mode)
        self.update_all_widgets()

    def convert_lincoin_to_linclue(self):
        USER_DATA.user_profile["lincoins"] -= DICT_CONVERSION_MONEY["price_lincoins"]
        USER_DATA.user_profile["linclues"] += DICT_CONVERSION_MONEY["reward_linclues"]
        USER_DATA.user_profile["cumulated_linclues"] += DICT_CONVERSION_MONEY["reward_linclues"]
        USER_DATA.save_changes()
        self.update_all_widgets()

    def buy_booster(self, number: int):
        """
        Buy a booster and update the display.

        Parameters
        ----------
        number : int
            Number of the booster to buy

        Returns
        -------
        None
        """
        print("I spend", DICT_AMOUNT_BUY[str(number)]["price"], "Euros")
        print("I get", DICT_AMOUNT_BUY[str(number)]["reward"], "Lincoins")
        popup = MessagePopup(
            title="Not implemented",
            center_label_text="This functionality will be implemented in a future version.",
            primary_color=self.primary_color,
            secondary_color=self.secondary_color,
            font_ratio=self.font_ratio
        )
        popup.open()
        # USER_DATA.user_profile["lincoins"] += DICT_AMOUNT_BUY[str(number)]["reward"]
        # USER_DATA.user_profile["cumulated_lincoins"] += DICT_AMOUNT_BUY[str(number)]["reward"]
        self.update_all_widgets()
