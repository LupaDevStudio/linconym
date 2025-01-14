"""
Module to create the act button.
"""

###############
### Imports ###
###############

### Python imports ###

from typing import (
    Callable
)
from threading import Thread

### Kivy imports ###

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty,
    BooleanProperty,
    ObjectProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_MUSICS
)
from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    SMALL_LABEL_FONT_SIZE,
    OPACITY_ON_BUTTON_PRESS,
    USER_DATA
)
from tools import (
    music_mixer
)
from screens.custom_widgets.popup import LoadingPopup

#############
### Class ###
#############


class MusicLayout(ButtonBehavior, RelativeLayout):
    """
    The music layout with a white round rectangle background.
    It is composed of a play/pause button on the left, a title.
    It can all be comprised of a buy/select button on the right.
    """

    background_color = ColorProperty(CUSTOM_BUTTON_BACKGROUND_COLOR)
    primary_color = ColorProperty()
    secondary_color = ColorProperty()
    music_title = StringProperty()
    music_price = NumericProperty()
    font_size = NumericProperty(SMALL_LABEL_FONT_SIZE)
    font_ratio = NumericProperty(1)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    radius = NumericProperty(20)
    is_playing = BooleanProperty(False)
    has_bought_music = BooleanProperty(False)
    is_using_music = BooleanProperty(False)
    release_function = ObjectProperty(lambda: 1 + 1)
    disable_button = BooleanProperty(False)

    def __init__(
            self,
            music_source: str,
            stop_playing_other_layouts: Callable,
            play_current_user_music: Callable,
            change_current_user_music: Callable = None,
            deselect_all_musics: Callable = None,
            music_id: str = "",
            **kwargs):
        super().__init__(**kwargs)

        self.music_source = music_source
        self.music_id = music_id
        self.stop_playing_other_layouts = stop_playing_other_layouts
        self.change_current_user_music = change_current_user_music
        self.play_current_user_music = play_current_user_music
        self.deselect_all_musics = deselect_all_musics

        self.always_release = True
        self.loading_popup = None

    def update_display(self):
        if self.has_bought_music:
            try:
                self.remove_widget(self.ids.buy_music_button)
            except:
                pass
            self.ids.select_music_button.opacity = 1
            self.ids.select_music_button.disable_button = False
        else:
            self.ids.buy_music_button.opacity = 1
            self.ids.buy_music_button.disable_button = False
            self.ids.select_music_button.opacity = 0
            self.ids.select_music_button.disable_button = True

    def disable_buy_select(self):
        """
        Disable the right part of the layout (for the credits screen).
        """
        self.remove_widget(self.ids.buy_music_button)
        self.remove_widget(self.ids.select_music_button)
        self.ids.music_title_label.size_hint = (0.8, 1)

    def load_sound(self):
        # Load the sound
        new_music = SoundLoader.load(
            PATH_MUSICS + self.music_source + ".mp3")
        music_mixer.add_sound(new_music, self.music_source)

        # Play the sound after loading
        Clock.schedule_once(self.play_sound)

    def play_sound(self, *_):
        # Close the loading popup if needed
        if self.loading_popup is not None:
            self.loading_popup.dismiss()
            self.loading_popup = None

        # Load the sound if needed
        if self.music_source not in music_mixer.musics:
            # Open a loading popup
            self.loading_popup = LoadingPopup(
                primary_color=self.primary_color,
                secondary_color=self.secondary_color,
                font_ratio=self.font_ratio
            )
            self.loading_popup.open()

            # Create a thread to load the sound
            background_thread = Thread(target=self.load_sound)
            background_thread.start()
            return

        if self.is_playing:
            self.play_current_user_music()
            self.is_playing = False
        else:
            self.stop_playing_other_layouts()
            self.is_playing = True
            if self.music_source not in music_mixer.musics:
                new_music = SoundLoader.load(
                    PATH_MUSICS + self.music_source + ".mp3")
                music_mixer.add_sound(new_music, self.music_source)
            music_mixer.change_volume(USER_DATA.settings["music_volume"])
            music_mixer.play(self.music_source, loop=True)

    def buy_music(self):
        bought_successfully = USER_DATA.buy_item(
            self.music_id, "music", self.music_price)
        if bought_successfully:
            self.get_root_window().children[0].get_screen(
                "musics").update_coins()
            self.has_bought_music = True
        self.update_display()

    def choose_music(self):
        self.deselect_all_musics()
        self.stop_playing_other_layouts()
        self.change_current_user_music(self.music_source)
        self.is_using_music = True

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y) and not (self.ids.play_pause_button.collide_point(self.last_touch.x, self.last_touch.y)):
                self.release_function()
            self.opacity = 1
