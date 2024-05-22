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
    NumericProperty,
    BooleanProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS
)
from tools.constants import (
    USER_DATA,
    THEMES_DICT,
    THEMES_RARITY_DICT
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
    has_bought_image = BooleanProperty()
    has_bought_colors = BooleanProperty()
    is_using_image = BooleanProperty()
    is_using_colors = BooleanProperty()

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

    def on_pre_enter(self, *args):
        self.coins_count = USER_DATA.user_profile["lincoins"]
        theme_rarity_code = THEMES_DICT[self.theme_key]["rarity"]
        self.image_price = THEMES_RARITY_DICT[theme_rarity_code]["image_price"]
        self.colors_price = THEMES_RARITY_DICT[theme_rarity_code]["colors_price"]
        self.both_price = self.colors_price + self.image_price
        self.is_using_image = USER_DATA.settings["current_theme_image"] == self.theme_key
        self.is_using_colors = USER_DATA.settings["current_theme_colors"] == self.theme_key
        if self.theme_key in USER_DATA.unlocked_themes:
            self.has_bought_image = USER_DATA.unlocked_themes[self.theme_key]["image"]
            self.has_bought_colors = USER_DATA.unlocked_themes[self.theme_key]["colors"]
        else:
            self.has_bought_image = False
            self.has_bought_colors = False
        self.update_display()
        return super().on_pre_enter(*args)
    
    def go_to_boosters(self):
        self.go_to_next_screen(
            screen_name="boosters",
            current_dict_kwargs={"theme_key": self.theme_key})
        
    def click_image(self):
        """
        Function to select the image of the theme.
        """
        if not self.has_bought_image:
            bought_sucessfully = USER_DATA.buy_item(
                self.theme_key, "image", self.image_price)
            if bought_sucessfully:
                self.has_bought_image = True
        elif self.has_bought_image and not self.is_using_image:
            USER_DATA.change_theme_image(self.theme_key)
            self.is_using_image = True
            self.update_backgrounds()
        self.update_display()
        

    def click_colors(self):
        """
        Function to select the colors of the theme.
        """
        if not self.has_bought_colors:
            bought_sucessfully = USER_DATA.buy_item(
                self.theme_key, "colors", self.colors_price)
            if bought_sucessfully:
                self.has_bought_colors = True
        elif self.has_bought_colors and not self.is_using_colors:
            USER_DATA.change_theme_colors(self.theme_key)
            self.is_using_colors = True
        self.update_display()

    def update_display(self):
        self.coins_count = USER_DATA.user_profile["lincoins"]
        self.ids["buy_image_button"].price = self.image_price
        self.ids["buy_image_button"].update_display()
        self.ids["buy_colors_button"].price = self.colors_price
        self.ids["buy_colors_button"].update_display()
    
    def update_backgrounds(self):
        current_theme_image = USER_DATA.settings["current_theme_image"]
        new_image = THEMES_DICT[current_theme_image]["image"]

        self.manager.change_all_background_images(
                PATH_BACKGROUNDS + new_image, include_themes_screen=True)
