"""
Module to create the tree to display the user progress on a level.
"""

###############
### Imports ###
###############

### Python imports ###

from typing import (
    Dict,
    List
)

### Kivy imports ###

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ColorProperty,
    ListProperty
)

### Local imports ###

from tools.basic_tools import argsort
from tools.kivy_tools import change_color_opacity
from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    WORD_BUTTON_HSPACING,
    WORD_BUTTON_VSPACING,
    WORD_BUTTON_SIDE_HOFFSET,
    WORD_BUTTON_SIDE_VOFFSET,
    WORD_BUTTON_BLOCK_HEIGHT_HINT,
    WORD_BUTTON_BLOCK_WIDTH_HINT
)
from tools.linconym import (
    get_parent_position,
    is_parent_of,
    get_word_position,
    has_end_word_in_children
)

test_words_found = ["sea", "sale", "sell", "shell", "sail", "snail",
                    "see", "bee", "tea", "pea", "peak", "keep", "tape", "pelt", "apes"]

test_position_to_word_id = {"0": 0, "0,0": 1, "0,0,0": 2,
                            "0,0,0,0": 3, "0,0,1": 4, "0,0,1,0": 5, "0,1": 6, "0,1,0": 7, "0,2": 8, "0,3": 9, "0,3,0": 10, "0,3,0,0": 11, "0,3,1": 12, "0,3,1,0": 13, "0,3,2": 14}


#################
### Functions ###
#################


def convert_str_position_to_tuple_position(str_position: str):
    """
    Convert a position under a string format to a tuple format.

    Parameters
    ----------
    str_position : str
        Position in a string format.

    Returns
    -------
    tuple
        Position in a tuple format.
    """

    str_elts = str_position.split(",")
    res = []
    for elt in str_elts:
        res.append(int(elt))
    res = tuple(res)

    return res


def build_sorted_positions_list(position_to_word_id: Dict[str, int]):
    """
    Extract and sort the positions to make sure parents are treated before there children.
    """

    positions_list = list(position_to_word_id.keys())
    sorted_positions_indices = argsort(positions_list)
    sorted_positions_list = [positions_list[i]
                             for i in sorted_positions_indices]

    return sorted_positions_list

###############
### Classes ###
###############


class WordLink(Widget):
    color = ColorProperty()
    font_ratio = NumericProperty(1)


class WordButton(ButtonBehavior, RelativeLayout):
    """
    A custom button with a colored round rectangle background.
    """

    background_color = ColorProperty()
    touch_color = ColorProperty()
    outline_color = ColorProperty()
    text = StringProperty()
    text_filling_ratio = NumericProperty(0.8)
    font_size = NumericProperty()
    font_ratio = NumericProperty(1)
    disable_button = BooleanProperty(False)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    has_check = BooleanProperty(False)

    def __init__(
            self,
            text_font_name=PATH_TEXT_FONT,
            font_ratio=None,
            current_position="",
            **kwargs):
        if font_ratio is not None:
            self.font_ratio = font_ratio
        super().__init__(**kwargs)
        self.always_release = True
        self.text_font_name = text_font_name
        self.current_position = current_position

    def on_press(self):
        if not self.disable_button:
            self.temp_color = self.background_color
            self.background_color = self.touch_color

    def on_release(self):
        if not self.disable_button:
            self.background_color = self.temp_color
            self.parent.change_to_word(self.current_position)


class TreeScrollview(ScrollView):
    """
    Class containing the scrollview to scroll over the tree.
    """

    font_ratio = NumericProperty(1)
    primary_color = ListProperty([0.5, 0.5, 0.5, 1.])
    secondary_color = ListProperty([1., 1., 1., 1.])

    def on_change_word_position_on_tree(self):
        self.parent.on_change_word_position_on_tree()

    def custom_scroll_to(self, widget, padding=10, animate=True):
        """
        Modified scroll to.

        Parameters
        ----------
        widget : _type_
            _description_
        padding : int, optional (default is 10)
            _description_
        animate : bool, optional (default is True)
            _description_
        """

        if not self.parent:
            return

        # if _viewport is layout and has pending operation, reschedule
        if hasattr(self._viewport, 'do_layout'):
            if self._viewport._trigger_layout.is_triggered:
                Clock.schedule_once(
                    lambda *dt: self.custom_scroll_to(widget, padding, animate))
                return

        if isinstance(padding, (int, float)):
            padding = (padding, padding)

        pos = self.parent.to_widget(*widget.to_window(*widget.pos))
        cor = self.parent.to_widget(*widget.to_window(widget.right,
                                                      widget.top))

        dx = dy = 0

        if pos[1] < self.y:
            dy = self.y - pos[1] + dp(padding[1])
        elif cor[1] > self.top:
            dy = self.top - cor[1] - dp(padding[1])

        if pos[0] < self.x:
            dx = self.x - pos[0] + dp(padding[0])
        elif cor[0] > self.right:
            dx = self.right - cor[0] - dp(padding[0])

        dsx, dsy = self.convert_distance_to_scroll(dx, dy)
        sxp = min(1, max(0, self.scroll_x - dsx))
        syp = min(1, max(0, self.scroll_y - dsy))

        if animate:
            if animate is True:
                animate = {'d': 0.2, 't': 'out_quad'}
            Animation.stop_all(self, 'scroll_x', 'scroll_y')
            vp = self._viewport
            if syp > 0 and vp.height > self.height:
                Animation(scroll_y=syp, **animate).start(self)
            if sxp > 0:
                Animation(scroll_x=sxp, **animate).start(self)
        else:
            self.scroll_x = sxp
            self.scroll_y = syp


class TreeLayout(RelativeLayout):
    """
    Class to create a tree layout to contain the user progress.
    """

    primary_color = ListProperty([0.5, 0.5, 0.5, 1.])
    secondary_color = ListProperty([1., 1., 1., 1.])
    font_ratio = NumericProperty(1)

    def __init__(
            self,
            **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = (None)
        self.size_hint_x = (None)
        self.bind(primary_color=self.on_primary_color_change)
        self.on_primary_color_change()
        self.bind(secondary_color=self.on_secondary_color_change)
        self.on_secondary_color_change()

        # Add a variable to control if the completed branches are displayed or not
        self.hide_completed_branches = False

    def mask_completed_branches(self):
        self.hide_completed_branches = True
        self.build_layout(
            position_to_word_id=self.position_to_word_id,
            words_found=self.words_found,
            current_position=self.current_position,
            end_word=self.end_word
        )

    def show_completed_branches(self):
        self.hide_completed_branches = False
        self.build_layout(
            position_to_word_id=self.position_to_word_id,
            words_found=self.words_found,
            current_position=self.current_position,
            end_word=self.end_word
        )

    def on_primary_color_change(self, base=None, widget=None, value=None):
        """
        Compute a transparent version of the primary color.
        """

        self.transparent_primary_color = change_color_opacity(
            self.primary_color, 0.7)

    def on_secondary_color_change(self, base=None, widget=None, value=None):
        """
        Compute a transparent version of the secondary color.
        """

        self.transparent_secondary_color = change_color_opacity(
            self.secondary_color, 0.7)

    def change_to_word(self, current_position):
        """
        Manage the word change when the user clicks on a word button on the tree.

        Parameters
        ----------
        current_word : str
            New current word.
        """

        if current_position is not None:
            self.change_current_position(current_position)

    def change_current_position(self, current_position):
        """
        Change the user position on the tree and update the display.

        Parameters
        ----------
        current_position : str
            String giving the new current position.
        """

        # Initialise two lists to store selected and unselected widgets
        selected_link_widgets = []
        unselected_link_widgets = []
        selected_word_widgets = []
        unselected_word_widgets = []

        # Update the current position variable
        self.current_position = current_position

        # Iterate over the stored positions
        for position in self.position_to_word_id.keys():
            # Skip if not included in word buttons dict
            if position not in self.word_button_dict:
                continue

            # Determine if the word is in the main branch
            is_main_branch = is_parent_of(
                position, child_position=current_position)
            is_selected = current_position == position

            if is_main_branch:
                main_color = self.primary_color
                touch_color = self.transparent_primary_color
                if is_selected:
                    outline_color = (1, 1, 1, 1)
                else:
                    outline_color = self.primary_color
            else:
                main_color = self.secondary_color
                outline_color = self.secondary_color
                touch_color = self.transparent_secondary_color

            # Apply the color changes to the word button
            word_button = self.word_button_dict[position]
            word_button.background_color = main_color
            word_button.outline_color = outline_color
            word_button.touch_color = touch_color

            if is_selected:
                widget_to_scroll_to = word_button

            # Apply the color changes to the word link
            if position in self.word_link_dict:
                word_link = self.word_link_dict[position]
                word_link.color = main_color

            # Store the widgets in the corresponding list
            if is_selected:
                selected_word_widgets.append(self.word_button_dict[position])
                if position in self.word_link_dict:
                    selected_link_widgets.append(self.word_link_dict[position])
            else:
                unselected_word_widgets.append(self.word_button_dict[position])
                if position in self.word_link_dict:
                    unselected_link_widgets.append(
                        self.word_link_dict[position])

        # Clear the current widgets
        self.clear_widgets()

        # Add all widgets in the appropriate order
        self.add_link_and_word_widgets(widget_to_scroll_to=widget_to_scroll_to)

        # Call a parent function to update
        self.parent.on_change_word_position_on_tree()

    def add_link_and_word_widgets(self, widget_to_scroll_to: WordButton | None = None):
        """
        Add all the widgets in the appropriate order for a nice display with selected items above.
        """

        # Add the unselected links
        for position in self.word_link_dict:
            if not is_parent_of(position, child_position=self.current_position):
                self.add_widget(self.word_link_dict[position])

        # Add the selected links
        for position in self.word_link_dict:
            if is_parent_of(position, child_position=self.current_position):
                self.add_widget(self.word_link_dict[position])

        # Add the unselected links
        for position in self.word_button_dict:
            if not is_parent_of(position, child_position=self.current_position):
                self.add_widget(self.word_button_dict[position])

        # Add the selected links
        for position in self.word_button_dict:
            if is_parent_of(position, child_position=self.current_position):
                self.add_widget(self.word_button_dict[position])

        # Scroll to a specific widget if needed
        if widget_to_scroll_to is not None:
            self.parent.custom_scroll_to(widget_to_scroll_to)

    def compute_word_button_pos_hint(self, current_rank, current_vertical_offset):
        """
        Compute the pos hint of the word button given its rank and offset.

        Parameters
        ----------
        current_rank : int
            Current rank of the word, indicate how far it is from the start word.
        current_vertical_offset : int
            Current vertical offset of the word.

        Returns
        -------
        dict
            Pos hint for the word button.
        """

        top = 1 - (self.side_voffset_hint +
                   current_vertical_offset * self.block_height_hint)
        left = self.side_hoffset_hint + \
            (current_rank - 1) * self.block_width_hint
        pos_hint = {"top": top, "x": left}

        return pos_hint

    def compute_word_link_pos_hint(
            self,
            current_rank: int,
            current_vertical_offset: int,
            parent_rank: int,
            parent_vertical_offset: int):
        """
        Compute the pos hint for a word link.

        Parameters
        ----------
        current_rank : int
            Rank of the current word.
        current_vertical_offset : int
            Vertical offset of the current word.
        parent_rank : int
            Rank of the parent word.
        parent_vertical_offset : int
            Vertical offset of the parent word.

        Returns
        -------
        dict
            Pos hint of the word link.
        """

        top = 1 - (self.side_voffset_hint + parent_vertical_offset *
                   self.block_height_hint + self.word_button_height_hint / 2)
        x = self.side_hoffset_hint + \
            (parent_rank - 1) * self.block_width_hint + \
            self.word_button_width_hint
        y = 1 - (self.side_voffset_hint + current_vertical_offset *
                 self.block_height_hint + self.word_button_height_hint / 2)
        right = x + WORD_BUTTON_HSPACING / self.rel_width

        pos_hint = {"top": top, "x": x}
        size_hint = (right - x, top - y)

        return pos_hint, size_hint

    def build_layout(
            self,
            position_to_word_id: Dict[str, int] = test_position_to_word_id,
            words_found: List[str] = test_words_found,
            current_position: str = "0,0,1,0",
            font_ratio: float = None,
            end_word: str = ""
    ):
        """
        Build the layout of the tree.

        Parameters
        ----------
        position_to_word_id : Dict[str, int]
            _description_
        words_found : List[str]
            _description_
        current_position : str
            _description_
        """

        # Update the font ratio
        if font_ratio is not None:
            self.font_ratio = font_ratio

        # Store the tree infos
        self.position_to_word_id = position_to_word_id.copy()
        self.words_found = words_found
        self.current_position = current_position
        self.end_word = end_word

        # Clean the position to word id dict if hide_completed_branches
        if self.hide_completed_branches:
            for key in list(position_to_word_id.keys()):
                if has_end_word_in_children(
                        current_position=key,
                        position_to_word_id=position_to_word_id,
                        words_found=words_found,
                        end_word=end_word) and key != "0":
                    position_to_word_id.pop(key)

        print(position_to_word_id)

        # Init a word button pile
        self.word_button_dict = {}

        # Init a word link pile
        self.word_link_dict = {}

        # Reorder the positions
        sorted_positions_list = build_sorted_positions_list(
            position_to_word_id)

        # Find the max rank
        max_rank = 0
        previous_rank = -1
        for position in sorted_positions_list:
            current_splitted_pos = position.split(",")
            current_rank = len(current_splitted_pos)
            if current_rank > max_rank:
                max_rank = current_rank
        self.max_rank = max_rank

        # Find the max vertical offset
        current_vertical_offset = 1
        for position in sorted_positions_list:
            current_rank = len(position.split(","))
            if current_rank <= previous_rank:
                current_vertical_offset += 1
            previous_rank = current_rank
        self.max_vertical_offset = current_vertical_offset

        # Define the size of the layout
        # TODO : make it depend on the size of the widget in pixels
        self.size = (self.max_rank * 160 * self.font_ratio,
                     self.max_vertical_offset * 40 * self.font_ratio)

        # Define the initial vertical offset
        current_vertical_offset = 0

        # Define the intial value for the previous rank
        previous_rank = -1

        # Create a dict to store the grid positions to plot the links
        position_to_grid_position = {}

        # Compute the relative size
        self.rel_width = WORD_BUTTON_SIDE_HOFFSET * 2 + \
            WORD_BUTTON_BLOCK_WIDTH_HINT * self.max_rank - WORD_BUTTON_HSPACING
        self.rel_height = WORD_BUTTON_SIDE_VOFFSET * 2 + \
            WORD_BUTTON_BLOCK_HEIGHT_HINT * self.max_vertical_offset - WORD_BUTTON_VSPACING

        # Compute the appropriate size
        self.word_button_width_hint = 1 / self.rel_width
        self.word_button_height_hint = 1 / self.rel_height
        self.block_width_hint = WORD_BUTTON_BLOCK_WIDTH_HINT / self.rel_width
        self.block_height_hint = WORD_BUTTON_BLOCK_HEIGHT_HINT / self.rel_height
        self.side_hoffset_hint = WORD_BUTTON_SIDE_HOFFSET / self.rel_width
        self.side_voffset_hint = WORD_BUTTON_SIDE_VOFFSET / self.rel_height

        # Iterate over the positions to display the widgets
        for position in sorted_positions_list:

            # Set the current rank
            current_rank = len(position.split(","))

            if current_rank <= previous_rank:
                current_vertical_offset += 1

            # Extract the corresponding word
            word_id = position_to_word_id[position]
            word = words_found[word_id]

            # Determine if the word is in the main branch
            is_main_branch = is_parent_of(
                position, child_position=current_position)
            is_selected = current_position == position

            if is_main_branch:
                main_color = self.primary_color
                touch_color = self.transparent_primary_color
                if is_selected:
                    outline_color = (1, 1, 1, 1)
                else:
                    outline_color = self.primary_color
            else:
                main_color = self.secondary_color
                outline_color = self.secondary_color
                touch_color = self.transparent_secondary_color

            # Compute the pos hint of the word button
            word_button_pos_hint = self.compute_word_button_pos_hint(
                current_rank=current_rank,
                current_vertical_offset=current_vertical_offset)

            # Verify if it belongs to a completed branch
            if not self.hide_completed_branches:
                has_check = has_end_word_in_children(
                    current_position=position,
                    position_to_word_id=position_to_word_id,
                    words_found=words_found,
                    end_word=end_word
                )
            else:
                has_check = False

            # Add the word widget
            word_button = WordButton(
                text=word,
                background_color=main_color,
                outline_color=outline_color,
                touch_color=touch_color,
                size_hint=(self.word_button_width_hint,
                           self.word_button_height_hint),
                pos_hint=word_button_pos_hint,
                font_ratio=self.font_ratio,
                current_position=position,
                has_check=has_check
            )

            if is_selected:
                widget_to_scroll_to = word_button

            # Recover the parent position
            parent_position = get_parent_position(position)
            if parent_position is not None:
                parent_rank, parent_vertical_offset = position_to_grid_position[parent_position]

                # Compute the pos hint of the link
                word_link_pos_hint, word_link_size_hint = self.compute_word_link_pos_hint(
                    current_rank=current_rank,
                    current_vertical_offset=current_vertical_offset,
                    parent_rank=parent_rank,
                    parent_vertical_offset=parent_vertical_offset)

                # Add the link with the parent
                word_link = WordLink(
                    color=main_color,
                    pos_hint=word_link_pos_hint,
                    size_hint=word_link_size_hint,
                    font_ratio=self.font_ratio
                )
                self.word_link_dict[position] = word_link

            self.word_button_dict[position] = word_button

            # Store the grid position
            position_to_grid_position[position] = (
                current_rank, current_vertical_offset)

            # Update the previous rank
            previous_rank = current_rank

        # Clear the layout
        self.clear_widgets()

        # Add all the widgets in the correct order
        self.add_link_and_word_widgets(widget_to_scroll_to=widget_to_scroll_to)

###############
### Testing ###
###############


if __name__ == "__main__":
    print(build_sorted_positions_list(test_position_to_word_id))
