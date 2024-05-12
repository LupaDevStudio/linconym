"""
Module to create the themes screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.clock import Clock

from kivy.properties import (
    NumericProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS
)
from tools.constants import (
    USER_DATA,
    THEMES_DICT,
    FPS,
    SCREEN_TITLE,
    SCREEN_BOTTOM_BAR,
    SCREEN_BACK_ARROW,
    SCREEN_TUTORIAL
)
from screens.custom_widgets import (
    LinconymScreen
)
from screens.custom_widgets import (
    ThemeLayout
)


#############
### Class ###
#############


class ThemesScreen(LinconymScreen):
    """
    Class to manage the themes screen.
    """

    dict_type_screen = {
        SCREEN_TITLE: "Themes",
        SCREEN_BOTTOM_BAR: "none",
        SCREEN_BACK_ARROW: "",
        SCREEN_TUTORIAL: ""
    }

    coins_count = NumericProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.THEME_LAYOUT_DICT = {}
        self.on_resize()
        self.fill_scrollview()

    def on_pre_enter(self, *args):
        self.coins_count = USER_DATA.user_profile["lincoins"]
        for theme_layout_id in self.THEME_LAYOUT_DICT:
            theme_layout:ThemeLayout = self.THEME_LAYOUT_DICT[theme_layout_id]
            theme_layout.update_display()
        return super().on_pre_enter(*args)

    def on_resize(self, *args):
        for act in self.THEME_LAYOUT_DICT:
            self.THEME_LAYOUT_DICT[act].font_ratio = self.font_ratio
        return super().on_resize(*args)

    def go_to_boosters(self):
        self.go_to_next_screen(screen_name="boosters")

    def update_coins(self):
        self.coins_count = USER_DATA.user_profile["lincoins"]

    def update_theme_layouts_display(self):
        """
        Update all theme widgets.
        """
        for theme in self.THEME_LAYOUT_DICT:
            self.THEME_LAYOUT_DICT[theme].update_display()

        current_theme_image = USER_DATA.settings["current_theme_image"]
        new_image = THEMES_DICT[current_theme_image]["image"]

        current_theme_colors = USER_DATA.settings["current_theme_colors"]
        self.primary_color = THEMES_DICT[current_theme_colors]["primary"]

        if (self.back_image_path != PATH_BACKGROUNDS + new_image and self.opacity_state == "main") \
                or (self.second_back_image_path != PATH_BACKGROUNDS + new_image and self.opacity_state == "second"):
            # Change the background image smoothly for this screen
            self.change_background(new_image)

            # Change the background image for all screens except this one
            self.manager.change_all_background_images(
                PATH_BACKGROUNDS + new_image)

    def change_background(self, new_image: str):
        """
        Change smoothly of background image.

        Parameters
        ----------
        new_image : str
            Name of the new image to set as background.

        Returns
        -------
        None
        """
        # Change the image of the background
        if self.opacity_state == "main":
            self.set_back_image_path(
                back_image_path=PATH_BACKGROUNDS + new_image,
                mode="second"
            )
        elif self.opacity_state == "second":
            self.set_back_image_path(
                back_image_path=PATH_BACKGROUNDS + new_image,
                mode="main"
            )

        # Schedule the change of the opacity to have a smooth transition
        Clock.schedule_interval(self.change_background_opacity, 1 / FPS)

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]
        # Load the widgets
        self.THEME_LAYOUT_DICT = {}
        for theme in THEMES_DICT:
            current_theme_button = ThemeLayout(
                theme_key=theme,
                source=PATH_BACKGROUNDS + THEMES_DICT[theme]["image"],
                font_ratio=self.font_ratio * 0.8)
            current_theme_button.update_display()
            self.THEME_LAYOUT_DICT[theme] = current_theme_button
            scrollview_layout.add_widget(self.THEME_LAYOUT_DICT[theme])

    def open_preview(self, theme_key):
        self.go_to_next_screen(
            screen_name="preview",
            next_dict_kwargs={"theme_key": theme_key}
        )
