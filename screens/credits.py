"""
Module to create the profile screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial
import webbrowser

### Kivy imports ###

from kivy.uix.label import Label

### Local imports ###

from tools.constants import (
    CREDITS_DICT,
    SCREEN_TITLE,
    SCREEN_BACK_ARROW,
    SCREEN_BOTTOM_BAR,
    CREDITS_CONTENT_SCROLLVIEW_FONT_SIZE,
    CREDITS_SCROLLVIEW_FONT_SIZE,
    TITLE_OUTLINE_COLOR,
    BUTTON_OUTLINE_WIDTH
)
from tools.path import (
    PATH_TITLE_FONT
)
from screens.custom_widgets import (
    LinconymScreen,
    CustomContentButton
)
from screens import (
    MusicLayout,
    IconCreditLayout,
    GeneralLicensesLayout,
    ImagesCreditLayout
)


#############
### Class ###
#############


class CreditsScreen(LinconymScreen):
    """
    Class to display the credits of the application.
    """

    dict_type_screen = {
        SCREEN_TITLE: "Credits",
        SCREEN_BACK_ARROW: "",
        SCREEN_BOTTOM_BAR: "none"
    }

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.fill_scrollview()

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()

    def fill_scrollview(self):
        # Load the widgets
        self.number_lines_credits = 0
        scrollview_layout = self.ids["scrollview_layout"]
        line_height = 50

        self.CREDITS_LAYOUT_DICT = {}

        # Add LupaDevStudio's team
        custom_content = CustomContentButton(
            title = "LupaDevStudio's Team",
            content = "Name 1 \nName 2 \nName 3 \nName 4",
            font_size_title=CREDITS_SCROLLVIEW_FONT_SIZE,
            font_size_content=CREDITS_CONTENT_SCROLLVIEW_FONT_SIZE,
            disable_button=True,
            font_ratio=self.font_ratio,
            size_hint_y=None,
            height=line_height * 2.5 * self.font_ratio
        )
        scrollview_layout.add_widget(custom_content)

        # Add the "copyright licenses" title
        title = "General licenses"
        my_label = Label(
            text = title,
            font_size = CREDITS_SCROLLVIEW_FONT_SIZE * self.font_ratio,
            color = (0, 0, 0, 1),
            outline_width=BUTTON_OUTLINE_WIDTH * self.font_ratio,
            outline_color=TITLE_OUTLINE_COLOR,
            font_name=PATH_TITLE_FONT,
            size_hint_y = None,
            height=line_height * self.font_ratio)
                         
        scrollview_layout.add_widget(my_label)

        # Add the general licenses
        license_dict = CREDITS_DICT["general_licenses"]
        for license in license_dict:
            title = license_dict[license]["title"]
            my_license = GeneralLicensesLayout(
                license_title = title,
                font_size = CREDITS_CONTENT_SCROLLVIEW_FONT_SIZE,
                font_ratio=self.font_ratio,
                radius=20,
                size_hint_y = None,
                height=line_height * self.font_ratio)
            licence_url = license_dict[license]["url"]
            my_license.release_function = partial(self.open_url, licence_url)
                  
            scrollview_layout.add_widget(my_license)

        # Add the "copyright images" title
        title = "Copyrights for images"
        my_label = Label(
            text = title,
            font_size = CREDITS_SCROLLVIEW_FONT_SIZE * self.font_ratio,
            color = (0, 0, 0, 1),
            outline_width=BUTTON_OUTLINE_WIDTH * self.font_ratio,
            outline_color=TITLE_OUTLINE_COLOR,
            font_name=PATH_TITLE_FONT,
            size_hint_y = None,
            height=line_height * self.font_ratio)
                         
        scrollview_layout.add_widget(my_label)

        # Add the images
        images_dict = CREDITS_DICT["image"]
        for image in images_dict:
            title = images_dict[image]["title"]
            url = images_dict[image]["url"]
            type = True if images_dict[image]["type"]=="icon" else False
            image_credit_layout = ImagesCreditLayout(
                image_title=title,
                current_image = image,
                icon_mode = type,
                font_ratio=self.font_ratio,
                radius=20,
                font_size=CREDITS_CONTENT_SCROLLVIEW_FONT_SIZE,
                size_hint_y = None,
                height=line_height * self.font_ratio)
            image_credit_layout.release_function = partial(self.open_url, url)
            self.CREDITS_LAYOUT_DICT[image] = image_credit_layout
            scrollview_layout.add_widget(image_credit_layout)

        # Add the "copyright icons" title
        title = "Copyrights for icons"
        my_label = Label(
            text = title,
            font_size = CREDITS_SCROLLVIEW_FONT_SIZE * self.font_ratio,
            color = (0, 0, 0, 1),
            outline_width=BUTTON_OUTLINE_WIDTH * self.font_ratio,
            outline_color=TITLE_OUTLINE_COLOR,
            font_name=PATH_TITLE_FONT,
            size_hint_y = None,
            height=line_height * self.font_ratio)

        scrollview_layout.add_widget(my_label)

        # Add the icons
        icons_dict = CREDITS_DICT["icons"]
        for icon in icons_dict:
            title = icons_dict[icon].split("\"")[4][1:-4]
            url = icons_dict[icon].split("\"")[1]
            icon_credit_layout = IconCreditLayout(
                icon_title=title,
                current_icon = icon,
                font_ratio=self.font_ratio,
                primary_color=self.primary_color,
                radius=20,
                font_size=CREDITS_CONTENT_SCROLLVIEW_FONT_SIZE,
                size_hint_y = None,
                height=line_height * self.font_ratio)
            icon_credit_layout.release_function = partial(self.open_url, url)
            self.CREDITS_LAYOUT_DICT[icon] = icon_credit_layout
            scrollview_layout.add_widget(icon_credit_layout)

        # add the "copyright music" title
        title = "Copyrights for musics"
        my_label = Label(
            text = title,
            font_size = CREDITS_SCROLLVIEW_FONT_SIZE * self.font_ratio,
            color=(0, 0, 0, 1),
            outline_width=BUTTON_OUTLINE_WIDTH * self.font_ratio,
            outline_color=TITLE_OUTLINE_COLOR,
            font_name=PATH_TITLE_FONT,
            size_hint_y = None,
            height=line_height * self.font_ratio)
        scrollview_layout.add_widget(my_label)

        # Add the musics
        musics_dict = CREDITS_DICT["musics"]
        for music in musics_dict:
            title = musics_dict[music]["name"] + \
                " – " + musics_dict[music]["author"]
            music_credit_layout = MusicLayout(
                music_title=title,
                font_ratio=self.font_ratio,
                primary_color=self.primary_color,
                radius=20,
                font_size=CREDITS_CONTENT_SCROLLVIEW_FONT_SIZE,
                size_hint_y = None,
                height=line_height * self.font_ratio)
            music_credit_layout.disable_buy_select()
            music_credit_layout.release_function = partial(
                self.open_url, musics_dict[music]["license"])
            self.CREDITS_LAYOUT_DICT[music] = music_credit_layout
            scrollview_layout.add_widget(music_credit_layout)

    def open_url(self, url):
        """
        Open the url given as argument.

        Parameters
        ----------
        url : str
            Url of the credit item.

        Returns
        -------
        None
        """
        webbrowser.open(url, 2)
