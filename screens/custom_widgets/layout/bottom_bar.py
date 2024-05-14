"""
Module to create the bottom bar with the buttons.
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ColorProperty
)

#############
### Class ###
#############


class BottomBar(RelativeLayout):
    """
    Class to create a bottom bar to quickly select a screen.
    """
    background_color = ColorProperty((0.1, 0.1, 0.1, 0.5))
    separation_color = ColorProperty((1, 1, 1, 1))
    # selected_color = (0.3, 0.3, 0.3, 0.7)
    selected_color = ColorProperty((0.1, 0.1, 0.1, 0.7))
    separation_height = 3
    button_width = 0.15
    button_height = 0.7
    selected = StringProperty()
    selected_rect_pos = ObjectProperty((0, 0))
    selected_rect_size = ObjectProperty((0, 0))

    def __init__(self, **kw):
        self.bind(selected=self.on_kv_post)
        super().__init__(**kw)

    def on_kv_post(self, base_widget, value=None):
        if self.selected + "_button" in self.ids.keys():
            self.selected_rect_pos = self.ids[self.selected +
                                              "_button"].pos_hint
            self.selected_rect_size = \
                (self.ids[self.selected + "_button"].size_hint[0] * 1.2,
                 self.ids[self.selected + "_button"].size_hint[1] * 1.2)
        else:
            self.selected_rect_pos = self.ids["home_button"].pos_hint
            self.selected_rect_size = (0, 0)
        return super().on_kv_post(base_widget)

    def open_home(self):
        """
        Open the home screen.
        """
        self.parent.manager.go_to_next_screen(next_screen_name="home")

    def open_settings(self):
        """
        Open the settings screen.
        """
        self.parent.manager.go_to_next_screen(next_screen_name="settings")

    def open_customization(self):
        """
        Open the customization screen.
        """
        self.parent.manager.go_to_next_screen(next_screen_name="customization")

    def open_profile(self):
        """
        Open the profile screen.
        """
        self.parent.manager.go_to_next_screen(next_screen_name="profile")
