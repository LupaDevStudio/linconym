"""
Module to create the quests screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty
)

### Local imports ###

from tools.constants import (
    SCREEN_BOTTOM_BAR,
    SCREEN_BACK_ARROW,
    SCREEN_TITLE,
    USER_STATUS_DICT,
    USER_DATA
)
from tools.path import (
    PATH_BADGES
)
from screens.custom_widgets import (
    LinconymScreen,
    BadgeLayout
)


#############
### Class ###
#############


class BadgesScreen(LinconymScreen):
    """
    Class to manage the screen that contains the profile information.
    """

    dict_type_screen = {
        SCREEN_TITLE: "Badges",
        SCREEN_BOTTOM_BAR: "none",
        SCREEN_BACK_ARROW: ""
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.fill_scrollview()

    def fill_scrollview(self):
        scrollview_layout = self.ids.scrollview_layout
        current_status = USER_DATA.user_profile["status"]
        list_status = list(USER_STATUS_DICT.keys())
        current_status_index = list_status.index(current_status)

        # Load the widgets
        self.BADGES_LAYOUT_DICT = {}
        for status_index in range(len(list_status)):
            if status_index <= current_status_index:
                name_status: str = list_status[status_index]
                title = name_status.capitalize()
                image_source = PATH_BADGES + name_status + ".png"
            else:
                title = "???"
                image_source = PATH_BADGES + "unknown.png"
            badge_layout = BadgeLayout(
                title=title,
                image_source=image_source,
                font_ratio=self.font_ratio,
                size_hint=(1/3, None),
                height=120*self.font_ratio
            )
            scrollview_layout.add_widget(badge_layout)

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
