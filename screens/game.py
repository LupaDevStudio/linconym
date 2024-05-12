"""
Module to create the game screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial
from typing import Literal

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty
)

### Local imports ###

from tools.constants import (
    USER_DATA,
    LETTER_FONT_SIZE,
    SCREEN_BACK_ARROW,
    SCREEN_TUTORIAL,
    GAMEPLAY_DICT
)
from screens.custom_widgets import (
    LinconymScreen,
    LevelCompletedPopup
)
from tools import (
    music_mixer
)
from screens import (
    ColoredRoundedButton
)
from tools.linconym import (
    ClassicGame
)

#############
### Class ###
#############


class GameScreen(LinconymScreen):
    """
    Class to manage the game screen.
    """

    current_level_name = StringProperty()
    dict_type_screen = {
        SCREEN_BACK_ARROW: "",
        SCREEN_TUTORIAL: ""
    }

    nb_stars = NumericProperty()
    start_word = StringProperty("")
    current_word = StringProperty("")
    new_word = StringProperty("")
    end_word = StringProperty("")
    start_to_end_label = StringProperty("")
    list_widgets_letters = []

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current_act_id: str
        self.current_level_id: str

    def reload_kwargs(self, dict_kwargs):
        self.current_act_id = dict_kwargs["current_act_id"]
        self.current_level_id = dict_kwargs["current_level_id"]

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        self.load_game_play()
        self.build_word()
        self.check_disable_keyboard()
        self.check_enable_submit_button()

    def reload_for_level_change(self, new_level_id: str):
        """
        Reload the components of the screen to continue playing on a new level.

        Parameters
        ----------
        new_level_id : str
            Id of the new level
        """

        # Save the data of the previous level
        self.save_data()

        # Assign the id for the new level
        self.current_level_id = new_level_id

        # Reload the components of the game
        self.load_game_play()
        self.build_word()
        self.check_disable_keyboard()
        self.check_enable_submit_button()

    def on_pre_leave(self, *args):
        # Clear the keyboard
        self.ids.keyboard_layout.destroy_keyboard()

        # Save the data
        self.save_data()

        return super().on_leave(*args)

    def save_data(self):

        # Insert data in save dict
        self.level_saved_data["current_position"] = self.game.current_position
        self.level_saved_data["words_found"] = self.game.words_found
        self.level_saved_data["position_to_word_id"] = self.game.position_to_word_id

        # Push changes to user data
        USER_DATA.classic_mode[self.current_act_id][self.current_level_id] = self.level_saved_data
        USER_DATA.save_changes()

    def check_disable_keyboard(self):

        # Disable the back button if we have nothing to delete
        if len(self.new_word) == 0:
            self.ids.keyboard_layout.disable_delete_button()
        else:
            self.ids.keyboard_layout.activate_delete_button()

        # Disable the letters is the word is already filled
        if len(self.new_word) >= len(self.current_word) + 1:
            self.ids.keyboard_layout.disable_letters()
        else:
            self.ids.keyboard_layout.activate_letters()

        # Disable everything if the current word is the final word
        if self.current_word.lower() == self.end_word:
            self.ids.keyboard_layout.disable_letters()
            self.ids.keyboard_layout.disable_delete_button()

    def check_enable_submit_button(self):
        """
        Enable the submit button if the word entered is valid.
        """

        if self.game.is_valid_and_new_in_path(
                new_word=self.new_word.lower()):
            self.enable_submit_button()
        else:
            self.disable_submit_button()

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
            self.new_word = self.new_word[:-1]

        # Add the new letter to the current word
        else:
            self.new_word += letter

        # Disable/Enable the keyboard and the submit button in consequence
        self.check_disable_keyboard()
        self.check_enable_submit_button()

        # Rebuild the display of the word
        self.build_word()

    def build_word(self):
        x_center = 0.5
        number_mandatory_letters = len(self.current_word) - 1
        number_letters = number_mandatory_letters + 2
        next_letter_counter = len(self.new_word)
        size_letter = 0.09
        horizontal_padding = 0.1 - size_letter
        height_letter = 0.05
        margin_left = 0

        # Adapt the size of the letters if there are too many
        if number_letters >= 11:
            size_letter = (0.95 - (number_letters - 1) *
                           horizontal_padding) / number_letters
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
                if counter_letter >= number_mandatory_letters:
                    outline_color = self.transparent_secondary_color
                else:
                    outline_color = self.secondary_color

            # Determine the content of the letter
            try:
                letter = self.new_word[counter_letter]
            except:
                letter = ""

            # Determine the x position of the letter
            if number_letters % 2 == 0:
                x_position = margin_left + x_center + \
                    (counter_letter - number_letters / 2 + 0.5) * horizontal_padding + \
                    (counter_letter - number_letters / 2) * size_letter
            else:
                x_position = margin_left + x_center + (counter_letter - number_letters / 2) * size_letter + (
                    counter_letter - number_letters / 2 - 0.5) * horizontal_padding

            # Create the letter widget
            letter_widget = ColoredRoundedButton(
                text=letter,
                background_color=(1, 1, 1, 1),
                pos_hint={"x": x_position, "y": 0.275},
                font_size=LETTER_FONT_SIZE,
                font_ratio=self.font_ratio,
                size_hint=(size_letter, height_letter),
                color_label=(0, 0, 0, 1),
                outline_color=outline_color,
                disable_button=True,
                outline_width=0.5
            )

            self.add_widget(letter_widget)
            self.list_widgets_letters.append(letter_widget)

    def on_change_word_position_on_tree(self):

        # Update the game to the new position
        self.game.change_position(self.ids["tree_layout"].current_position)

        # Recover the current word
        self.current_word = self.game.current_word.upper()

        # Update the new word
        self.new_word = self.new_word[:len(self.current_word) + 1]

        # Update the keyboard and submit button
        self.check_disable_keyboard()
        self.check_enable_submit_button()

    def load_game_play(self):

        # Clean the new word
        self.new_word = ""

        # Store the dict containing the user progress
        self.level_saved_data = USER_DATA.classic_mode[self.current_act_id][self.current_level_id]

        # Save the dict containing the level instructions
        self.level_info = GAMEPLAY_DICT[self.current_act_id][self.current_level_id]

        # Extract start word and end word
        self.start_word = self.level_info["start_word"]
        self.end_word = self.level_info["end_word"]
        self.start_to_end_label = (
            self.start_word + " > " + self.end_word).upper()

        self.transparent_secondary_color = [
            self.secondary_color[0], self.secondary_color[1], self.secondary_color[2], 0.3]
        self.ids.keyboard_layout.build_keyboard()

        self.nb_stars = USER_DATA.classic_mode[self.current_act_id][self.current_level_id]["nb_stars"]

        temp = self.current_act_id.replace("Act", "")
        self.current_level_name = "Act " + temp + " – " + self.current_level_id

        # Extract the tree data from the saved data
        if "current_position" in self.level_saved_data and "words_found" in self.level_saved_data and "position_to_word_id" in self.level_saved_data:
            current_position = self.level_saved_data["current_position"]
            words_found = self.level_saved_data["words_found"]
            position_to_word_id = self.level_saved_data["position_to_word_id"]
        else:
            current_position = None
            words_found = None
            position_to_word_id = None

        # Create a game instance
        self.game = ClassicGame(
            act_id=self.current_act_id,
            lvl_id=self.current_level_id,
            current_position=current_position,
            position_to_word_id=position_to_word_id,
            words_found=words_found
        )

        # Build the tree
        self.build_tree_layout()

        # Define the current word
        self.current_word = self.game.current_word.upper()

    def build_tree_layout(self):
        """
        Build the layout of the tree showing the words found.
        """

        self.ids["tree_layout"].build_layout(
            position_to_word_id=self.game.position_to_word_id,
            words_found=self.game.words_found,
            current_position=self.game.current_position
        )

    def submit_word(self):
        self.game.submit_word(self.new_word.lower())
        self.build_tree_layout()

        # Save the data
        self.save_data()

        # Change the current and new word
        if not self.check_level_complete():
            self.current_word = self.new_word
            self.new_word = ""

            # Enable the keyboard and disable the submit button
            self.build_word()
            self.check_disable_keyboard()

            self.disable_submit_button()
        else:
            end_level_dict = self.game.on_level_completed()
            self.nb_words = end_level_dict["nb_words"]
            # Update the stars
            self.nb_stars = end_level_dict["stars"]
            self.display_success_popup()

    def display_success_popup(self):

        # Check if there is a next level in the same act
        next_lvl_id = str(int(self.current_level_id) + 1)
        has_next_levels_in_act = next_lvl_id in GAMEPLAY_DICT[self.current_act_id]

        # Create the popup for the completion
        popup = LevelCompletedPopup(
            primary_color=self.primary_color,
            secondary_color=self.secondary_color,
            font_ratio=self.font_ratio,
            top_label_text=f"Solution found in {self.nb_words} words.",
            nb_stars=self.nb_stars,
            new_level=True,
            current_level_text=f"Level {self.current_level_id}",
            percentage_experience_before=0.2,  # TODO change
            percentage_experience_won=0.1,  # TODO change
            experience_displayed=10,  # TODO change
            next_level_function=partial(
                self.reload_for_level_change, next_lvl_id),
            has_next_levels_in_act=has_next_levels_in_act,
            number_lincoins_won=10, # TODO change
            number_linclues_won=1 # TODO change
        )
        popup.open()

    def check_level_complete(self):
        # The level is complete
        if self.new_word == self.end_word.upper():
            # self.current_word = self.start_word.upper()
            self.ids.keyboard_layout.disable_whole_keyboard()
            self.disable_submit_button()
            self.new_word = ""
            return True
        return False

    def enable_submit_button(self):
        self.ids.submit_button.opacity = 1
        self.ids.submit_button.disable_button = False

    def disable_submit_button(self):
        self.ids.submit_button.opacity = 0
        self.ids.submit_button.disable_button = True

    def go_to_quests_screen(self):
        dict_kwargs = {
            "current_level_id": self.current_level_id,
            "current_act_id": self.current_act_id
        }
        self.go_to_next_screen(
            screen_name="quests",
            current_dict_kwargs=dict_kwargs,
            next_dict_kwargs=dict_kwargs)

    def go_to_configure_tree_screen(self):
        dict_kwargs = {
            "current_level_id": self.current_level_id,
            "current_act_id": self.current_act_id
        }
        self.go_to_next_screen(
            screen_name="configure_tree",
            current_dict_kwargs=dict_kwargs,
            next_dict_kwargs=dict_kwargs)
