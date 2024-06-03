"""
Module to create the game screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial
from threading import Thread

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty
)
from kivy.clock import Clock

### Local imports ###

from tools.constants import (
    USER_DATA,
    LETTER_FONT_SIZE,
    SCREEN_BACK_ARROW,
    SCREEN_TUTORIAL,
    GAMEPLAY_DICT,
    GAMEPLAY_LEGEND_DICT,
    TUTORIAL,
    GAME_TUTORIAL_DICT,
    USER_STATUS_DICT,
    MAX_NB_LETTERS
)
from screens.custom_widgets import (
    LinconymScreen,
    LevelCompletedPopup,
    LincluesPopup,
    LevelUpPopup,
    TutorialPopup,
    LoadingPopup
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
from tools.levels import (
    compute_lincoins_when_level_up
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
    allow_delete_current_word = BooleanProperty(False)
    list_widgets_letters = []
    keyboard_mode = StringProperty(USER_DATA.settings["keyboard_mode"])
    mode = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current_act_id: str
        self.current_level_id: str
        self.level_saved_data = {}

    def reload_kwargs(self, dict_kwargs):
        self.current_act_id = dict_kwargs["current_act_id"]
        self.current_level_id = dict_kwargs["current_level_id"]
        self.mode = dict_kwargs["mode"]

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.keyboard_mode = USER_DATA.settings["keyboard_mode"]
        self.ids.tree_layout.hide_completed_branches = USER_DATA.settings[
            "hide_completed_branches"]

        self.load_game_play()
        self.build_word()
        self.check_disable_keyboard()
        self.check_enable_submit_button()
        self.check_delete_current_word()
        self.save_data()

    # Override tutorial to have a special tutorial at the beginning

    def open_tutorial(self, screen_name):
        tutorial_to_display = "all_rules"
        if self.current_act_id == "1":
            if self.current_level_id in GAME_TUTORIAL_DICT:
                tutorial_to_display = GAME_TUTORIAL_DICT[self.current_level_id]
                if tutorial_to_display == "more_complicated_puzzles" and not USER_DATA.tutorial["game"][tutorial_to_display]:
                    USER_DATA.user_profile["linclues"] += 5
                    USER_DATA.user_profile["cumulated_linclues"] += 5
                    USER_DATA.save_changes()

        popup = TutorialPopup(
            primary_color=self.primary_color,
            secondary_color=self.secondary_color,
            title=TUTORIAL[screen_name][tutorial_to_display]["title"],
            tutorial_content=TUTORIAL[screen_name][tutorial_to_display]["tutorial_content"],
            font_ratio=self.font_ratio)
        popup.open()

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
        self.check_tutorial_to_open()

    def on_pre_leave(self, *args):
        # Take screenshot for adv
        # self.export_to_png("test.png", scale=2.732)

        # Clear the keyboard
        self.ids.keyboard_layout.destroy_keyboard()

        # Save the data
        self.save_data()

        return super().on_leave(*args)

    def save_data(self):

        self.level_saved_data = {}

        if self.mode == "classic":
            for key in USER_DATA.classic_mode[self.current_act_id][self.current_level_id]:
                self.level_saved_data[key] = USER_DATA.classic_mode[self.current_act_id][self.current_level_id][key]

        elif self.mode == "legend":
            for key in USER_DATA.legend_mode[self.current_act_id][self.current_level_id]:
                self.level_saved_data[key] = USER_DATA.legend_mode[self.current_act_id][self.current_level_id][key]

        # Insert data in save dict
        self.level_saved_data["current_position"] = self.game.current_position
        self.level_saved_data["words_found"] = self.game.words_found
        self.level_saved_data["position_to_word_id"] = self.game.position_to_word_id

        # Push changes to user data
        if self.mode == "classic":
            USER_DATA.classic_mode[self.current_act_id][self.current_level_id] = self.level_saved_data.copy()
        elif self.mode == "legend":
            USER_DATA.legend_mode[self.current_act_id][self.current_level_id] = self.level_saved_data.copy()

        USER_DATA.save_changes()

    def check_disable_keyboard(self):

        # Disable the back button if we have nothing to delete
        if len(self.new_word) == 0:
            self.ids.keyboard_layout.disable_delete_button()
        else:
            self.ids.keyboard_layout.activate_delete_button()

        # Disable the letters is the word is already filled
        if len(self.new_word) >= len(self.current_word) + 1 or len(self.new_word) >= MAX_NB_LETTERS:
            self.ids.keyboard_layout.disable_letters()
        else:
            self.ids.keyboard_layout.activate_letters()

        # Disable everything if the current word is the final word
        if self.current_word.lower() == self.end_word:
            self.ids.keyboard_layout.disable_letters()
            self.ids.keyboard_layout.disable_delete_button()
            # Remove the letters widgets
            for letter_widget in self.list_widgets_letters:
                self.remove_widget(letter_widget)

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
            if len(self.new_word) < MAX_NB_LETTERS:
                self.new_word += letter

        # Disable/Enable the keyboard and the submit button in consequence
        self.check_disable_keyboard()
        self.check_enable_submit_button()

        # Rebuild the display of the word
        self.build_word()

    def build_word(self):
        x_center = 0.5
        number_mandatory_letters = len(self.current_word) - 1
        number_letters = min(number_mandatory_letters + 2, MAX_NB_LETTERS)
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
                release_function=partial(self.pop_letter, counter_letter)
            )

            self.add_widget(letter_widget)
            self.list_widgets_letters.append(letter_widget)

    def check_delete_current_word(self, *_):
        """
        Verify if the current word can be deleted.
        """

        if self.game.get_nb_next_words(self.game.current_position) == 0\
                and self.current_word != self.start_word.upper() \
            and self.current_word != self.end_word.upper():
            self.allow_delete_current_word = True
            self.ids.delete_word_button.opacity = 1
        else:
            self.allow_delete_current_word = False
            self.ids.delete_word_button.opacity = 0

    def pop_letter(self, letter_id):
        if letter_id < len(self.new_word):
            self.new_word = self.new_word[:letter_id] + \
                self.new_word[letter_id + 1:]

            # Disable/Enable the keyboard and the submit button in consequence
            self.check_disable_keyboard()
            self.check_enable_submit_button()

            # Rebuild the display of the word
            self.build_word()

    def on_change_word_position_on_tree(self):

        # Update the game to the new position
        self.game.change_position(self.ids["tree_layout"].current_position)

        # Recover the current word
        self.current_word = self.game.current_word.upper()

        # Update the new word
        self.new_word = self.new_word[:len(self.current_word) + 1]

        # Update the keyboard and submit button
        self.build_word()
        self.check_disable_keyboard()
        self.check_enable_submit_button()
        self.check_delete_current_word()

    def load_game_play(self):

        # Clean the new word
        self.new_word = ""

        # Store the dict containing the user progress
        if self.mode == "classic":
            self.level_saved_data = USER_DATA.classic_mode[self.current_act_id][self.current_level_id].copy()

            # Save the dict containing the level instructions
            self.level_info = GAMEPLAY_DICT[self.current_act_id][self.current_level_id]
        elif self.mode == "legend":
            self.level_saved_data = USER_DATA.legend_mode[self.current_act_id][self.current_level_id].copy()

            # Save the dict containing the level instructions
            self.level_info = GAMEPLAY_LEGEND_DICT[self.current_act_id][self.current_level_id]

        # Extract start word and end word
        self.start_word = self.level_info["start_word"]
        self.end_word = self.level_info["end_word"]
        self.start_to_end_label = (
            self.start_word + " > " + self.end_word).upper()

        self.transparent_secondary_color = [
            self.secondary_color[0], self.secondary_color[1], self.secondary_color[2], 0.3]
        self.ids.keyboard_layout.build_keyboard()

        if self.mode == "classic":
            self.nb_stars = USER_DATA.classic_mode[self.current_act_id][self.current_level_id]["nb_stars"]
        elif self.mode == "legend":
            self.nb_stars = USER_DATA.legend_mode[self.current_act_id][self.current_level_id]["nb_stars"]

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
            position_to_word_id=self.game.position_to_word_id.copy(),
            words_found=self.game.words_found,
            current_position=self.game.current_position,
            end_word=self.end_word.lower()
        )

    def submit_word(self):
        self.game.submit_word(self.new_word.lower())

        # Save the data
        self.save_data()

        # Change the current and new word
        if not self.check_level_complete():
            # Rebuild layout
            self.build_tree_layout()

            self.current_word = self.new_word
            self.new_word = ""

            # Enable the keyboard and disable the submit button
            self.build_word()
            self.check_disable_keyboard()

            self.disable_submit_button()
        else:
            end_level_dict = self.game.on_level_completed()

            # Update the stars
            self.nb_stars = max(end_level_dict["stars"], self.nb_stars)

            # Clear the new word field
            self.new_word = ""
            self.build_word()

            # Switch back to root
            self.game.current_position = "0"

            # Rebuild layout
            self.build_tree_layout()

            # Display the popup for the level completion
            self.display_success_popup(end_level_dict=end_level_dict)

        self.check_delete_current_word()
        self.on_change_word_position_on_tree()

        # Save the data
        self.save_data()

    def display_success_popup(self, end_level_dict):

        # Check if there is a next puzzle in the same act
        next_lvl_id = str(int(self.current_level_id) + 1)

        if self.mode == "classic":
            has_next_levels_in_act = next_lvl_id in GAMEPLAY_DICT[self.current_act_id]
        elif self.mode == "legend":
            has_next_levels_in_act = next_lvl_id in GAMEPLAY_LEGEND_DICT[self.current_act_id]

        if has_next_levels_in_act:
            right_button_label = "Next puzzle"
            next_level_function = partial(
                self.reload_for_level_change, next_lvl_id)
        else:
            right_button_label = "Return to menu"
            screen_name = "classic_mode"
            if self.mode == "legend":
                screen_name = "legend_mode"
            next_level_function = partial(
                self.go_to_next_screen,
                screen_name=screen_name,
                current_dict_kwargs={
                    "current_act_id": self.current_act_id,
                    "current_level_id": self.current_level_id,
                    "mode": self.mode}
                )

        # Create the popup for the completion
        popup = LevelCompletedPopup(
            title=f"Puzzle {self.current_level_id} completed",
            primary_color=self.primary_color,
            secondary_color=self.secondary_color,
            right_button_label=right_button_label,
            font_ratio=self.font_ratio,
            top_label_text=f"Solution found in {end_level_dict['nb_words']} words.",
            nb_stars=end_level_dict["stars"],
            new_level=end_level_dict["has_level_up"],
            current_level_text=f"Level {USER_DATA.user_profile['level']}",
            percentage_experience_before=end_level_dict["previous_level_progress"],
            percentage_experience_won=end_level_dict["current_level_progress"] -
            end_level_dict["previous_level_progress"],
            experience_displayed=end_level_dict["xp_earned"],
            next_level_function=next_level_function,
            number_lincoins_won=end_level_dict["lincoins_earned"],
            number_linclues_won=end_level_dict["linclues_earned"]
        )
        popup.open()

        # Create the popup for level up
        if end_level_dict["has_level_up"]:
            user_level = USER_DATA.user_profile['level']
            current_status = USER_DATA.user_profile["status"]
            has_changed_status = False
            list_status = list(USER_STATUS_DICT.keys())
            index_current_status = list_status.index(current_status)
            next_status = list_status[index_current_status + 1]
            if current_status != "legend" and user_level > USER_STATUS_DICT[current_status]["end"]:
                has_changed_status = True
                USER_DATA.user_profile["status"] = next_status
                USER_DATA.save_changes()

            size_hint_popup = (
                0.85, 0.6) if has_changed_status else (0.85, 0.3)
            popup = LevelUpPopup(
                primary_color=self.primary_color,
                secondary_color=self.secondary_color,
                number_lincoins_won=compute_lincoins_when_level_up(
                    USER_DATA.user_profile["status"]),
                has_changed_status=has_changed_status,
                size_hint=size_hint_popup,
                current_status=current_status,
                next_status=next_status,
                font_ratio=self.font_ratio
            )
            popup.open()

    def check_level_complete(self):
        # The level is complete
        if self.new_word == self.end_word.upper():
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
            "current_act_id": self.current_act_id,
            "mode": self.mode
        }
        self.go_to_next_screen(
            screen_name="quests",
            current_dict_kwargs=dict_kwargs,
            next_dict_kwargs=dict_kwargs)

    def go_to_configure_tree_screen(self):
        dict_kwargs = {
            "current_level_id": self.current_level_id,
            "current_act_id": self.current_act_id,
            "mode": self.mode
        }
        self.save_data()
        self.go_to_next_screen(
            screen_name="configure_tree",
            current_dict_kwargs=dict_kwargs,
            next_dict_kwargs=dict_kwargs)

    def delete_current_word(self):
        """
        Delete the current word.
        """

        # Delete the current word in game instance
        self.game.delete_current_word()

        # Reset the new word
        self.new_word = ""

        # Load the parent word
        self.current_word = self.game.current_word.upper()

        # Enable the keyboard and disable the submit button
        self.build_word()
        self.build_tree_layout()
        self.check_disable_keyboard()
        self.check_enable_submit_button()

        # Save the data
        self.save_data()

        Clock.schedule_once(self.check_delete_current_word)

    def ask_to_use_linclues(self):
        if "nb_hints_used" not in USER_DATA.classic_mode[self.current_act_id][self.current_level_id]:
            nb_hints = 0
        else:
            nb_hints = USER_DATA.classic_mode[self.current_act_id][self.current_level_id]["nb_hints_used"]

        # Compute the number of linclues to use
        number_linclues_to_use = 1 + nb_hints

        # Display the popup
        popup = LincluesPopup(
            primary_color=self.primary_color,
            secondary_color=self.secondary_color,
            font_ratio=self.font_ratio,
            number_linclues_to_use=number_linclues_to_use,
            number_linclues=USER_DATA.user_profile["linclues"],
            yes_function=partial(self.use_linclues, number_linclues_to_use),
            game=self.game
        )
        popup.open()

    def use_linclues(self, number_linclues_to_use):
        # Decrease the amount of linclues
        USER_DATA.user_profile["linclues"] -= number_linclues_to_use

        # Increase the number of hints used
        if "nb_hints_used" not in USER_DATA.classic_mode[self.current_act_id][self.current_level_id]:
            USER_DATA.classic_mode[self.current_act_id][self.current_level_id]["nb_hints_used"] = 1
        else:
            USER_DATA.classic_mode[self.current_act_id][self.current_level_id]["nb_hints_used"] += 1

        # Display a loading popup
        self.loading_popup = LoadingPopup(
            primary_color=self.primary_color,
            secondary_color=self.secondary_color,
            font_ratio=self.font_ratio
        )
        self.loading_popup.open()

        # Create a thread
        background_thread = Thread(target=self.search_hint_word)
        background_thread.start()

    def search_hint_word(self):
        # Get the solution word
        hint_word = self.game.get_hint()

        # Schedule submission
        Clock.schedule_once(partial(self.submit_hint_word, hint_word))

    def submit_hint_word(self, hint_word: str, *_):
        # Close the loading popup
        self.loading_popup.dismiss()

        # Submit it
        self.new_word = hint_word.upper()
        self.submit_word()

        # Save data
        USER_DATA.save_changes()
