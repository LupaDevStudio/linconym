"""
Module to create the act button.
"""

###############
### Imports ###
###############

from functools import partial

### Kivy imports ###
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    ColorProperty,
    BooleanProperty
)

### Local imports ###

from tools.path import (
    PATH_TITLE_FONT
)
from tools.constants import (
    CUSTOMIZATION_LAYOUT_FONT_SIZE,
    CUSTOM_BUTTON_BACKGROUND_COLOR
)

#############
### Class ###
#############


class BoosterLayout(RelativeLayout):
    """
    A layout to display the boosters.
    """

    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    mode = StringProperty()  # can be "ads" or "buy"
    booster_title = StringProperty()
    font_size = NumericProperty(CUSTOMIZATION_LAYOUT_FONT_SIZE)
    font_ratio = NumericProperty(1)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    list_ads_buy = ListProperty()
    first_color = ColorProperty((1, 1, 1, 1))
    second_color = ColorProperty((0, 0, 0, 1))
    third_color = ColorProperty((0, 0, 0, 1))
    first_disable = BooleanProperty()
    second_disable = BooleanProperty()
    third_disable = BooleanProperty()
    first_text = StringProperty()
    second_text = StringProperty()
    third_text = StringProperty()
    first_amount_text = StringProperty()
    second_amount_text = StringProperty()
    third_amount_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(list_ads_buy=self.update_colors_disabled)

    def update_colors_disabled(self, base_widget, value):
        for counter in range(len(self.list_ads_buy)):
            element = self.list_ads_buy[counter]
            if counter == 0:
                self.first_color = element["color"]
                self.first_disable = element["disable_button"]
                if "price" in element:
                    self.first_text = str(element["price"]) + "€"
                self.first_amount_text = str(element["amount"])
            elif counter == 1:
                self.second_color = element["color"]
                self.second_disable = element["disable_button"]
                if "price" in element:
                    self.second_text = str(element["price"]) + "€"
                self.second_amount_text = str(element["amount"])
            elif counter == 2:
                self.third_color = element["color"]
                self.third_disable = element["disable_button"]
                if "price" in element:
                    self.third_text = str(element["price"]) + "€"
                self.third_amount_text = str(element["amount"])
        self.ids.first_circle.release_function = partial(self.choose_item, 1)
        self.ids.second_circle.release_function = partial(self.choose_item, 2)
        self.ids.third_circle.release_function = partial(self.choose_item, 3)

    def choose_item(self, number):
        if self.mode == "ads":
            self.parent.see_ad(number)
        elif self.mode == "buy":
            self.parent.buy_booster(number)
