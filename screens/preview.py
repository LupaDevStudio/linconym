"""
Module to create the preview screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    ColorProperty,
    NumericProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS
)
from tools.constants import (
    USER_DATA,
    THEMES_DICT
)
from tools.kivy_tools import (
    ImprovedScreen
)


#############
### Class ###
#############


class PreviewScreen(ImprovedScreen):
    """
    Class to manage the screen that contains the profile information.
    """

    primary_color = ColorProperty((0, 0, 0, 1))
    secondary_color = ColorProperty((0, 0, 0, 1))
    theme_key = StringProperty()
    coins_count = NumericProperty()
    colors_price = NumericProperty()
    image_price = NumericProperty()
    both_price = NumericProperty()

    def __init__(self, **kwargs) -> None:
        current_theme_image = USER_DATA.settings["current_theme_image"]
        super().__init__(
            back_image_path=PATH_BACKGROUNDS +
            THEMES_DICT[current_theme_image]["image"],
            **kwargs)

    def reload_kwargs(self, dict_kwargs):
        self.theme_key = dict_kwargs["theme_key"]
        self.set_back_image_path(back_image_path=PATH_BACKGROUNDS + THEMES_DICT[self.theme_key]["image"])
        self.primary_color = THEMES_DICT[self.theme_key]["primary"]
        self.secondary_color = THEMES_DICT[self.theme_key]["secondary"]

    def on_enter(self, *args):
        self.coins_count = USER_DATA.user_profile["coins"]
        self.colors_price = THEMES_DICT[self.theme_key]["colors_price"]
        self.image_price = THEMES_DICT[self.theme_key]["image_price"]
        self.both_price = self.colors_price + self.image_price
        return super().on_enter(*args)
    
    def go_to_boosters(self):
        self.go_to_next_screen(
            screen_name="boosters",
            current_dict_kwargs={"theme_key": self.theme_key})
        
    def buy_both(self):
        self.go_backwards()

    def buy_image(self):
        self.go_backwards()

    def buy_colors(self):
        self.go_backwards()