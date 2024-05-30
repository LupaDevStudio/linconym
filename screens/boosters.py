"""
Module to create the profile screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial
from typing import Literal
from random import randint
import datetime

### Kivy imports ###

from kivy.properties import (
    NumericProperty,
    ListProperty
)
from kivy.clock import mainthread

### Local imports ###

from tools.constants import (
    USER_DATA,
    SCREEN_TUTORIAL,
    AMOUNT_DAILY_ADS,
    AMOUNT_UNLIMITED_ADS,
    AMOUNT_WEEKLY_AD,
    DICT_CONVERSION_MONEY,
    DICT_AMOUNT_BUY,
    SCREEN_BACK_ARROW,
    SCREEN_BOTTOM_BAR,
    SCREEN_TITLE
)
from screens.custom_widgets import (
    LinconymScreen,
    MessagePopup,
    RewardPopup,
    ConversionPopup
)
from tools.linconym import (
    AD_CONTAINER
)
from tools import (
    music_mixer,
    sound_mixer
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
    list_unlimited_ads = ListProperty()
    list_weekly_ads = ListProperty()
    list_conversion = ListProperty()
    list_buy = ListProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        last_day_date = USER_DATA.ads["current_day_date"]
        last_week_date = USER_DATA.ads["current_week_date"]
        current_day_date = datetime.date.today()
        diff = current_day_date.weekday()
        current_week_date = current_day_date - datetime.timedelta(days=diff)
        current_day_date = current_day_date.strftime('%m/%d/%Y')
        current_week_date = current_week_date.strftime('%m/%d/%Y')

        if last_day_date != current_day_date:
            USER_DATA.ads["current_day_date"] = current_day_date
            USER_DATA.ads["number_daily_ads_left"] = 3
            USER_DATA.ads["has_seen_daily_wheel"] = False

        if last_week_date != current_week_date:
            USER_DATA.ads["current_week_date"] = current_week_date
            USER_DATA.ads["number_weekly_ads_left"] = 1

        self.update_all_widgets()

    def on_enter(self, *args):
        super().on_enter(*args)

    def update_all_widgets(self):
        self.lincoins_count = USER_DATA.user_profile["lincoins"]
        self.linclues_count = USER_DATA.user_profile["linclues"]
        self.build_list_daily_ads()
        self.build_list_unlimited_ads()
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

    def build_list_unlimited_ads(self):
        self.list_unlimited_ads = []
        circle_color = self.primary_color

        self.list_unlimited_ads.append({
            "reward": AMOUNT_UNLIMITED_ADS,
            "circle_color": circle_color,
            "disable_button": False,
            "release_function": partial(self.see_ad, "unlimited")
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
            "release_function": self.ask_convert_lincoin_to_linclue
        })

    def build_list_buy(self):
        temp_list = []
        self.list_buy = []
        for counter in range(1, len(DICT_AMOUNT_BUY) + 1):
            temp_list.append({
                "circle_color": self.primary_color,
                "reward": [{"lincoin": DICT_AMOUNT_BUY[str(counter)]["reward"]}],
                "price_unit": "€",
                "price": DICT_AMOUNT_BUY[str(counter)]["price"],
                "release_function": partial(self.buy_booster, counter)
            })
        self.list_buy = temp_list

    def see_ad(self, mode: Literal["daily", "weekly", "unlimited"]):
        """
        Launch the ad and update the display.

        Parameters
        ----------
        mode : Literal["daily", "weekly", "unlimited"]
            Mode according to which it is a daily, unlimited or weekly ad.
        """
        music_mixer.change_volume(new_volume=0)
        sound_mixer.change_volume(new_volume=0)

        AD_CONTAINER.watch_ad(ad_callback=partial(
            self.display_ad_award, mode), ad_fail=self.display_ad_not_found)

    @mainthread
    def display_ad_not_found(self):
        """
        Display a popup explaining that no ad could be found.
        """

        popup = MessagePopup(
            title="Unable to load ads",
            center_label_text="The loading of the ads failed, please try again.",
            primary_color=self.primary_color,
            secondary_color=self.secondary_color,
            font_ratio=self.font_ratio
        )
        popup.open()

    @mainthread
    def display_ad_award(self, mode: Literal["daily", "weekly", "unlimited"]):
        """
        Display a popup to show the reward.

        Parameters
        ----------
        mode : Literal["daily", "weekly", "unlimited"]
            Mode according to which it is a daily, unlimited or weekly ad.
        """

        # Compute the reward.
        if mode == "weekly":
            nb_linclues = AMOUNT_WEEKLY_AD[0]["linclue"]
            nb_lincoins = AMOUNT_WEEKLY_AD[0]["lincoin"]
        elif mode == "unlimited":
            nb_lincoins = AMOUNT_UNLIMITED_ADS[0]["lincoin"]
            nb_linclues = 0
        else:
            reward_id = randint(0, 2)
            if "linclue" in AMOUNT_DAILY_ADS[reward_id]:
                nb_linclues = AMOUNT_DAILY_ADS[reward_id]["linclue"]
            else:
                nb_linclues = 0
            if "lincoin" in AMOUNT_DAILY_ADS[reward_id]:
                nb_lincoins = AMOUNT_DAILY_ADS[reward_id]["lincoin"]
            else:
                nb_lincoins = 0

        # Open a popup to show the reward
        reward_function = partial(
            self.give_ad_award,
            mode=mode,
            nb_linclues=nb_linclues,
            nb_lincoins=nb_lincoins
        )
        reward_popup = RewardPopup(
            reward_function=reward_function,
            font_ratio=self.font_ratio,
            primary_color=self.primary_color,
            secondary_color=self.secondary_color,
            number_lincoins_won=nb_lincoins,
            number_linclues_won=nb_linclues
        )
        reward_popup.open()

        music_mixer.change_volume(
            new_volume=USER_DATA.settings["music_volume"])
        sound_mixer.change_volume(
            new_volume=USER_DATA.settings["sound_volume"])

    def give_ad_award(self, mode: Literal["daily", "weekly", "unlimited"], nb_linclues: int, nb_lincoins: int):
        """
        Give the reward from the ad and update the display.

        Parameters
        ----------
        mode : Literal["daily", "unlimited", "weekly"]
            Mode according to which it is a daily, unlimited or weekly ad.
        nb_linclues : int
            Number of linclues to give.
        nb_lincoins : int
            Number of lincoins to give.
        """

        # Give the award
        USER_DATA.user_profile["lincoins"] += nb_lincoins
        USER_DATA.user_profile["cumulated_lincoins"] += nb_lincoins
        USER_DATA.user_profile["linclues"] += nb_linclues
        USER_DATA.user_profile["cumulated_linclues"] += nb_linclues

        # Update number of ads left
        USER_DATA.change_boosters(mode)

        # Reload an add
        AD_CONTAINER.load_ad()

        # Update the display
        self.update_all_widgets()

    def ask_convert_lincoin_to_linclue(self):
        popup = ConversionPopup(
            yes_function=self.convert_lincoin_to_linclue,
            font_ratio=self.font_ratio,
            primary_color=self.primary_color,
            secondary_color=self.secondary_color
        )
        popup.open()

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
