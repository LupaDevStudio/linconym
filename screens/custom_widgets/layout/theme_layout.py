"""
Module to create the theme selection layout.
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.uix.image import Image
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ColorProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    CUSTOMIZATION_LAYOUT_FONT_SIZE,
    USER_DATA,
    THEMES_DICT,
    RARITY_THEMES_COLORS_DICT
)

#############
### Class ###
#############


class ThemeLayout(Image):
    """
    A layout to select the image or the colors of a theme.
    """

    theme_title = StringProperty()
    theme_rarity = StringProperty()
    font_size = NumericProperty(CUSTOMIZATION_LAYOUT_FONT_SIZE)
    font_ratio = NumericProperty(1)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    primary_color = ColorProperty([1, 1, 1, 1])
    secondary_color = ColorProperty([0, 0, 0, 1])
    theme_rarity_color = ColorProperty([1, 1, 1, 1])
    has_bought_image = BooleanProperty()
    has_bought_colors = BooleanProperty()
    is_using_image = BooleanProperty()
    is_using_colors = BooleanProperty()

    outside_radius = NumericProperty(30)
    inside_radius = NumericProperty(10)

    def __init__(self, theme_key: str = "", **kwargs):

        if theme_key not in THEMES_DICT:
            theme_key = THEMES_DICT.keys()[0]

        self.theme_key = theme_key
        self.theme_title = THEMES_DICT[theme_key]["name"]
        self.theme_rarity = THEMES_DICT[theme_key]["rarity"]
        self.theme_rarity_color = RARITY_THEMES_COLORS_DICT[self.theme_rarity]
        self.image_price = THEMES_DICT[theme_key]["image_price"]
        self.colors_price = THEMES_DICT[theme_key]["colors_price"]
        self.primary_color = THEMES_DICT[theme_key]["primary"]
        self.secondary_color = THEMES_DICT[theme_key]["secondary"]

        self.update_variables()

        super().__init__(**kwargs)

    def update_variables(self):
        """
        Update the variables to indicate if a component is selected or unlocked.
        """
        if self.theme_key in USER_DATA.unlocked_themes:
            self.has_bought_image = USER_DATA.unlocked_themes[self.theme_key]["image"]
            self.has_bought_colors = USER_DATA.unlocked_themes[self.theme_key]["colors"]
            if USER_DATA.settings["current_theme_image"] == self.theme_key:
                self.is_using_image = True
            else:
                self.is_using_image = False
            if USER_DATA.settings["current_theme_colors"] == self.theme_key:
                self.is_using_colors = True
            else:
                self.is_using_colors = False
        else:
            self.has_bought_image = False
            self.has_bought_colors = False
            self.is_using_image = False
            self.is_using_colors = False

    def update_display(self):
        self.update_variables()
        self.ids["buy_image_button"].price = self.image_price
        self.ids["buy_image_button"].update_display()
        self.ids["buy_colors_button"].price = self.colors_price
        self.ids["buy_colors_button"].update_display()

    def click_image(self):
        """
        Function to select the image of the theme.
        """
        if not self.has_bought_image:
            bought_sucessfully = USER_DATA.buy_item(
                self.theme_key, "image", self.image_price)
            if bought_sucessfully:
                self.get_root_window().children[0].get_screen(
                    "themes").update_coins()
                self.has_bought_image = True
            self.update_display()
        elif self.has_bought_image and not self.is_using_image:
            USER_DATA.change_theme_image(self.theme_key)
            self.get_root_window().children[0].get_screen(
                "themes").update_theme_layouts_display()

    def click_colors(self):
        """
        Function to select the colors of the theme.
        """
        if not self.has_bought_colors:
            bought_sucessfully = USER_DATA.buy_item(
                self.theme_key, "colors", self.colors_price)
            if bought_sucessfully:
                self.get_root_window().children[0].get_screen(
                    "themes").update_coins()
                self.has_bought_colors = True
            self.update_display()
        elif self.has_bought_colors and not self.is_using_colors:
            USER_DATA.change_theme_colors(self.theme_key)
        self.update_display()
        self.get_root_window().children[0].get_screen(
            "themes").update_theme_layouts_display()

    def open_preview(self):
        self.get_root_window().children[0].get_screen(
            "themes").open_preview(self.theme_key)
