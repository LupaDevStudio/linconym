"""
Module to create the profile screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    NumericProperty,
    ListProperty
)

### Local imports ###

from tools.constants import (
    USER_DATA,
    SCREEN_TUTORIAL,
    DICT_AMOUNT_ADS,
    DICT_AMOUNT_BUY,
    SCREEN_BACK_ARROW,
    SCREEN_BOTTOM_BAR,
    SCREEN_TITLE
)
from screens.custom_widgets import (
    LinconymScreen
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

    coins_count = NumericProperty()
    list_ads = ListProperty()
    list_buy = ListProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.coins_count = USER_DATA.user_profile["lincoins"]
        self.build_list_ads()
        self.build_list_buy()

    def build_list_ads(self):
        self.list_ads = []
        for ad in USER_DATA.ads:
            if USER_DATA.ads[ad]:
                self.list_ads.append({
                    "color": self.secondary_color,
                    "disable_button": True,
                    "amount": DICT_AMOUNT_ADS[ad]
                })
            else:
                self.list_ads.append({
                    "color": self.primary_color,
                    "disable_button": False,
                    "amount": DICT_AMOUNT_ADS[ad]
                })

    def build_list_buy(self):
        self.list_buy = []
        for counter in range(1, 4):
            self.list_buy.append({
                "color": self.primary_color,
                "disable_button": False,
                "amount": DICT_AMOUNT_BUY[str(counter)]["amount"],
                "price": DICT_AMOUNT_BUY[str(counter)]["price"]
            })

    def see_ad(self, number: int):
        """
        Launch the ad and update the display.

        Parameters
        ----------
        number : int
            Number of the ad to watch

        Returns
        -------
        None
        """
        USER_DATA.change_boosters(number)
        self.build_list_ads()

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
        pass
