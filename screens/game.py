"""
Module to create the game screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS
)
from tools.constants import (
    USER_DATA,
    THEMES_DICT,
    LETTER_FONT_SIZE
)
from tools.kivy_tools import (
    ImprovedScreen,
)
from tools import (
    music_mixer
)
from screens import (
    ColoredRoundedButton
)

#############
### Class ###
#############


class GameScreen(ImprovedScreen):
    """
    Class to manage the game screen.
    """

    current_level_name = StringProperty()
    nb_stars = NumericProperty()
    primary_color = ColorProperty((0, 0, 0, 1))
    secondary_color = ColorProperty((0, 0, 0, 1))
    previous_word = StringProperty("BOY")
    current_word = StringProperty("J")
    list_widgets_letters = []

    def __init__(self, **kwargs) -> None:
        current_theme_image = USER_DATA.settings["current_theme_image"]
        super().__init__(
            back_image_path=PATH_BACKGROUNDS +
            THEMES_DICT[current_theme_image]["image"],
            **kwargs)
        self.current_act_id: str
        self.current_level_id: str

    def on_pre_enter(self, *args):
        current_theme_colors = USER_DATA.settings["current_theme_colors"]
        self.primary_color = THEMES_DICT[current_theme_colors]["primary"]
        self.secondary_color = THEMES_DICT[current_theme_colors]["secondary"]
        self.ids.keyboard_layout.build_keyboard()
        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        temp = self.current_act_id.replace("Act", "")
        self.current_level_name = "Act " + temp + " – " + self.current_level_id
        self.load_game_play()
        self.load_game_user()
        self.build_word()
        self.check_disable_keyboard()
        return super().on_enter(*args)

    def check_disable_keyboard(self):

        # Disable the back button if we have nothing to delete
        if len(self.current_word) == 0:
            self.ids.keyboard_layout.disable_delete_button()
        else:
            self.ids.keyboard_layout.activate_delete_button()

        # Disable the letters is the word is already filled
        if len(self.current_word) >= len(self.previous_word) + 2:
            self.ids.keyboard_layout.disable_letters()
        else:
            self.ids.keyboard_layout.activate_letters()

    def touch_letter(self, letter):
        """
        React when a letter of the keyboard is released.
        
        Parameters
        ----------
        letter : str
            Letter pressed. Can be any letter in capital or "DELETE".
        
        Returns
        -------
        None
        """
        # Delete the last letter of the current word
        if letter == "DELETE":
            self.current_word = self.current_word[:-1]
        
        # Add the new letter to the current word
        else:
            self.current_word += letter

        # Disable the keyboard in consequence
        self.check_disable_keyboard()

        # Rebuild the display of the word
        self.build_word()

    def build_word(self):
        x_center = 0.5
        number_mandatory_letters = len(self.previous_word)
        number_letters = number_mandatory_letters + 2
        next_letter_counter = len(self.current_word)
        horizontal_padding = 0.02
        size_letter = 0.07
        height_letter = 0.05
        margin_left = 0

        # Adapt the size of the letters if there are too many
        if number_letters >= 11:
            size_letter = (0.95 - (number_letters-1)*horizontal_padding)/number_letters
            margin_left = 0.025

        # Remove the previous widgets
        for letter_widget in self.list_widgets_letters:
            self.remove_widget(letter_widget)

        # Create the letters
        for counter_letter in range(number_letters):

            # Determine the color of the outline
            if counter_letter == next_letter_counter:
                outline_color = self.primary_color
            else:
                outline_color = self.secondary_color
            
            # Determine the content of the letter
            try:
                letter = self.current_word[counter_letter]
            except:
                letter = ""

            # Determine the x position of the letter
            if number_letters % 2 == 0:
                x_position = margin_left + x_center + (counter_letter-number_letters/2+0.5)*horizontal_padding + (counter_letter-number_letters/2)*size_letter
            else:
                x_position = margin_left + x_center + (counter_letter-number_letters/2)*size_letter + (counter_letter-number_letters/2-0.5)*horizontal_padding

            # Create the letter widget
            letter_widget = ColoredRoundedButton(
                text=letter,
                background_color=(1,1,1,1),
                pos_hint={"x": x_position,"y": 0.35},
                font_size=LETTER_FONT_SIZE,
                font_ratio=self.font_ratio,
                size_hint=(size_letter, height_letter),
                color_label=(0,0,0,1),
                outline_color=outline_color,
                disable_button=True
            )

            self.add_widget(letter_widget)
            self.list_widgets_letters.append(letter_widget)

    def load_game_play(self):
        pass

    def load_game_user(self):
        pass