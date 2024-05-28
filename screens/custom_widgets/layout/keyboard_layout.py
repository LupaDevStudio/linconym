"""
Module to create the theme selection layout.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty,
    ObjectProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_ICONS
)
from tools.constants import (
    LETTER_FONT_SIZE
)
from screens.custom_widgets import (
    ColoredRoundedButton,
    ColoredRoundedButtonImage
)

#############
### Class ###
#############


class KeyboardLayout(RelativeLayout):
    """
    The keyboard layout.
    """

    font_size = NumericProperty(LETTER_FONT_SIZE)
    font_ratio = NumericProperty(1)
    horizontal_padding = NumericProperty(1)
    size_letter = NumericProperty(0.09)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    background_color = ColorProperty([1, 1, 1, 1])
    touch_color = ColorProperty([0, 0, 0, 1])
    keyboard_mode = StringProperty("QWERTY")
    touch_function = ObjectProperty()
    delete_key = None
    list_letter_keys = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.horizontal_padding = (1 - 10*self.size_letter) / 9

        self.bind(horizontal_padding=self.update_padding)
        self.bind(size_letter=self.update_padding)

        self.disable_color = [self.background_color[0],
                              self.background_color[1], self.background_color[2], 0.5]

    def update_padding(self, base_widget, value):
        # Because maximum of 9 letters in line
        self.size_letter = (1 - self.horizontal_padding * 9) / 10

    def build_keyboard(self):
        """
        Add the different letters and the delete button in the keyboard layout.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.destroy_keyboard()
        self.list_letter_keys = []

        vertical_padding = 0.04
        height_letter = (1 - vertical_padding * 3) / 3

        # Define the type of the keyboard
        if self.keyboard_mode == "QWERTY":
            first_line_letters = ["Q", "W", "E",
                                  "R", "T", "Y", "U", "I", "O", "P"]
            second_line_letters = ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
            third_line_letters = ["Z", "X", "C", "V", "B", "N", "M"]
            first_margin = 0
            second_margin = (self.size_letter + self.horizontal_padding) / 2
            third_margin = (self.size_letter + self.horizontal_padding) / 2
        elif self.keyboard_mode == "AZERTY":
            first_line_letters = ["A", "Z", "E",
                                  "R", "T", "Y", "U", "I", "O", "P"]
            second_line_letters = ["Q", "S", "D",
                                   "F", "G", "H", "J", "K", "L", "M"]
            third_line_letters = ["W", "X", "C", "V", "B", "N"]
            first_margin = 0
            second_margin = 0
            third_margin = self.size_letter + self.horizontal_padding

        # First line
        counter = 0
        for letter in first_line_letters:
            colored_rounded_button = ColoredRoundedButton(
                text=letter,
                background_color=self.background_color,
                touch_color=self.touch_color,
                pos_hint={
                    "x": first_margin + counter * (self.horizontal_padding + self.size_letter),
                    "y": 2 * vertical_padding + 2 * height_letter},
                font_size=self.font_size,
                font_ratio=self.font_ratio,
                size_hint=(self.size_letter, height_letter),
                color_label=(1, 1, 1, 1),
                outline_color=(1, 1, 1, 1),
                release_function=partial(self.touch_letter, letter)
            )
            self.add_widget(colored_rounded_button)
            self.list_letter_keys.append(colored_rounded_button)
            counter += 1

        # Second line
        counter = 0
        for letter in second_line_letters:
            colored_rounded_button = ColoredRoundedButton(
                text=letter,
                background_color=self.background_color,
                touch_color=self.touch_color,
                pos_hint={
                    "x": second_margin + counter * (self.horizontal_padding + self.size_letter),
                    "y": vertical_padding + height_letter},
                font_size=self.font_size,
                font_ratio=self.font_ratio,
                size_hint=(self.size_letter, height_letter),
                color_label=(1, 1, 1, 1),
                outline_color=(1, 1, 1, 1),
                release_function=partial(self.touch_letter, letter)
            )
            self.add_widget(colored_rounded_button)
            self.list_letter_keys.append(colored_rounded_button)
            counter += 1

        # Third line
        counter = 0
        for letter in third_line_letters:
            colored_rounded_button = ColoredRoundedButton(
                text=letter,
                background_color=self.background_color,
                touch_color=self.touch_color,
                pos_hint={
                    "x": third_margin + counter * (self.horizontal_padding + self.size_letter),
                    "y": 0},
                font_size=self.font_size,
                font_ratio=self.font_ratio,
                size_hint=(self.size_letter, height_letter),
                color_label=(1, 1, 1, 1),
                outline_color=(1, 1, 1, 1),
                release_function=partial(self.touch_letter, letter)
            )
            self.add_widget(colored_rounded_button)
            self.list_letter_keys.append(colored_rounded_button)
            counter += 1

        # DELETE key
        self.delete_key = ColoredRoundedButtonImage(
            image_path=PATH_ICONS + "delete.png",
            background_color=self.background_color,
            touch_color=self.touch_color,
            pos_hint={
                "x": third_margin + counter * (self.horizontal_padding + self.size_letter),
                "y": 0},
            font_ratio=self.font_ratio,
            size_hint=(self.size_letter * 2 +
                       self.horizontal_padding, height_letter),
            color_image=(1, 1, 1, 1),
            release_function=partial(self.touch_letter, "DELETE")
        )
        self.add_widget(self.delete_key)

    def destroy_keyboard(self):
        """
        Remove all the keys of the keyboard.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for letter in self.list_letter_keys:
            self.remove_widget(letter)
        if self.delete_key is not None:
            self.remove_widget(self.delete_key)

    def disable_delete_button(self):
        """
        Disable the delete button.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # self.delete_key.background_color = DISABLE_BUTTON_COLOR
        self.delete_key.opacity = 0.7
        self.delete_key.disabled = True

    def activate_delete_button(self):
        """
        Enable the delete button.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.delete_key.opacity = 1
        self.delete_key.disabled = False
        # self.delete_key.background_color = self.background_color

    def disable_letters(self):
        """
        Disable the buttons of the letters.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        letter_key: ColoredRoundedButton
        for letter_key in self.list_letter_keys:
            # letter_key.background_color = DISABLE_BUTTON_COLOR
            letter_key.disabled = True
            # letter_key.opacity = 0.5

    def activate_letters(self):
        """
        Enable the buttons of the letters.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        letter_key: ColoredRoundedButton
        for letter_key in self.list_letter_keys:
            letter_key.disabled = False
            # letter_key.background_color = self.background_color
            # letter_key.opacity = 1

    def disable_whole_keyboard(self):
        """
        Disable the whole keyboard.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.disable_delete_button()
        self.disable_letters()

    def activate_whole_keyboard(self):
        """
        Activate the whole keyboard.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.activate_letters()
        self.activate_delete_button()

    def touch_letter(self, letter, *args):
        """
        Activate the function when a letter is pressed in the keyboard.

        Parameters
        ----------
        letter : string
            Letter, it can be a capital letter or "DELETE"

        Returns
        -------
        None
        """
        self.touch_function(letter)
