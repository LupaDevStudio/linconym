"""
Main module of Linconym.
"""

###############
### Imports ###
###############

### Python imports ###

import os

### Kivy imports ###

# Disable back arrow
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from kivy.uix.screenmanager import (
    ScreenManager,
    NoTransition,
    Screen
)
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock

### Local imports ###

from tools.path import (
    PATH_IMAGES,
    PATH_TEMP_IMAGES
)
from tools.constants import (
    ANDROID_MODE,
    FPS,
    MSAA_LEVEL
)
import screens.opening

###############
### General ###
###############


class WindowManager(ScreenManager):
    """
    Screen manager, which allows the navigation between the different menus.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        self.list_previous_screens = []
        current_screen = Screen(name="temp")
        self.add_widget(current_screen)
        self.current = "temp"

    def change_all_background_images(self, new_image_path, include_themes_screen=False):
        for screen_name in self.screen_names:
            if screen_name != "temp" and (screen_name != "themes" or include_themes_screen):
                screen = self.get_screen(screen_name)
                screen.set_back_image_path(new_image_path)

    def go_to_previous_screen(self):
        if len(self.list_previous_screens) != 0:
            previous_screen = self.list_previous_screens.pop()
            screen_name = previous_screen[0]
            self.get_screen(screen_name).reload_kwargs(previous_screen[1])
            self.current = screen_name

    def go_to_next_screen(self, next_screen_name, current_dict_kwargs={}, next_dict_kwargs={}):
        current_screen_name = self.current
        self.list_previous_screens.append(
            (current_screen_name, current_dict_kwargs))
        self.get_screen(next_screen_name).reload_kwargs(next_dict_kwargs)
        self.current = next_screen_name


class MainApp(App, Widget):
    """
    Main class of the application.
    """

    def build_config(self, config):
        """
        Build the config file for the application.

        It sets the FPS number and the antialiasing level.
        """
        config.setdefaults('graphics', {
            'maxfps': str(FPS),
            'multisamples': str(MSAA_LEVEL)
        })

    def build(self):
        """
        Build the application.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        Window.clearcolor = (0, 0, 0, 1)
        self.icon = PATH_IMAGES + "logo.png"

    def on_resume(self):
        current_screen_name = self.root_window.children[0].current
        self.root_window.children[0].get_screen(current_screen_name).refresh()
        return super().on_resume()

    def on_stop(self):
        temp_images_list = os.listdir(PATH_TEMP_IMAGES)
        for temp_image in temp_images_list:
            if temp_image.endswith(".png"):
                os.remove(PATH_TEMP_IMAGES + temp_image)
        return super().on_stop()

    def on_start(self):
        if ANDROID_MODE:
            Window.update_viewport()

        # Open the opening screen
        opening_screen = screens.opening.OpeningScreen(name="opening")
        self.root_window.children[0].add_widget(opening_screen)
        self.root_window.children[0].current = "opening"

        Clock.schedule_once(
            self.root_window.children[0].get_screen("opening").launch_thread)

        print("Main app started")

        return super().on_start()


# Run the application
if __name__ == "__main__":
    if not ANDROID_MODE:
        Window.size = (405, 720)
        # Window.size = (750, 1000)
    MainApp().run()
