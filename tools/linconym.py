"""
Module containing the core of Linconym.
"""

###############
### Imports ###
###############

### Python imports ###

if __name__ == "__main__":
    import sys
    sys.path.append("../")
    sys.path.append("./")

from typing import (
    Dict,
    List,
    Callable
)
import time

### Local imports ###

from tools.path import (
    PATH_GAMEPLAY,
    PATH_RESOURCES
)
from tools.constants import (
    ENGLISH_WORDS_DICTS,
    GAMEPLAY_DICT,
    GAMEPLAY_LEGEND_DICT,
    USER_DATA,
    XP_PER_CLASSIC_PUZZLE,
    XP_PER_LEGEND_PUZZLE,
    DICT_ID_LIST,
    NB_LINCOINS_PER_STAR_CLASSIC_DICT,
    NB_LINCOINS_PER_STAR_LEGEND_DICT,
    REWARD_AD,
    ANDROID_MODE,
    IOS_MODE,
    MAX_NB_LETTERS
)
from tools.basic_tools import (
    dichotomy,
    save_json_file,
    load_json_file
)
from tools.levels import (
    compute_progression
)
if ANDROID_MODE:
    from tools.kivads import (
        RewardedInterstitial,
        RewardedAd,
        TestID
    )

if IOS_MODE:
    from pyobjus import autoclass  # pylint: disable=import-error # type: ignore


#################
### Constants ###
#################

# keys to access user data
NB_WORDS_KEY: str = "best_solution_nb_words"
STARS_KEY: str = "nb_stars"
XP_KEY: str = "experience"
QUEST_WORD_KEY: str = "quest_word_done"

#################
### Functions ###
#################


def get_parent_position(position: str):
    """
    Compute the parent position of the given position.

    Parameters
    ----------
    position : str
        Position of the word in the tree.

    Returns
    -------
    str or None
        Position of the parent word or None if the root position is given in input.
    """

    splitted_pos = position.split(",")
    parent_splitted_pos = splitted_pos[:-1]
    if len(parent_splitted_pos) == 0:
        return None
    else:
        parent_pos = ""
        for i in range(len(parent_splitted_pos) - 1):
            parent_pos += parent_splitted_pos[i] + ","
        parent_pos += parent_splitted_pos[-1]
        return parent_pos


def is_parent_of(position, child_position):
    """
    Check if the given position is parent of the given child position.

    Parameters
    ----------
    position : _type_
        Position to check.
    child_position : _type_
        Position of the potential child.

    Returns
    -------
    bool
        Boolean indication if the given position is parent or not.
    """

    # Convert both positions to tuple
    t_child_pos = convert_str_pos_to_tuple_pos(child_position)
    t_parent_pos = convert_str_pos_to_tuple_pos(position)

    # Check if the common branch match
    res = t_child_pos[:len(t_parent_pos)] == t_parent_pos

    return res


def get_word_position(input_word: str, position_to_word_id: Dict[str, int], words_found: List[str]):
    """
    Get the position of the given word.

    Parameters
    ----------
    input_word : str
        Input word.
    position_to_word_id : Dict[str, int]
        Dictionary containing positions for each word index.
    words_found : List[str]
        List of all words founds.

    Returns
    -------
    str or None
        Position or None if the word is not included in the list.
    """
    for i, word in enumerate(words_found):
        if input_word == word:
            word_index = i
    for index, position in enumerate(position_to_word_id):
        if index == word_index:
            return position
    return None


def convert_str_pos_to_tuple_pos(position: str):
    """
    Convert a position described as a string to a position described as a tuple.
    """

    res = []
    split_pos = position.split(",")
    for el in split_pos:
        res.append(int(el))

    # print(position, res)

    return tuple(res)


def get_children(current_position: str, position_to_word_id: dict):
    """
    Find all the direct children of the given position.
    """

    # Create the list of children
    res = []

    # Iterate over the positions in the tree
    for position in position_to_word_id:
        if is_parent_of(current_position, position) and len(position) > len(current_position):
            res.append(position)

    return res


def has_end_word_in_children(
        current_position: str,
        position_to_word_id: dict,
        words_found: list,
        end_word: str):
    """
    Verify if the end word is in the descendance.

    Parameters
    ----------
    current_position : str
        Current position on the tree.
    position_to_word_id : dict
        _description_
    words_found : list
        _description_
    end_word : str
        _description_

    Returns
    -------
    """

    # Initialize the pile
    pile = [current_position]

    # Iterate while there are children
    while len(pile) > 0:
        # Extract an element
        current_position = pile.pop(0)
        word_id = position_to_word_id[current_position]

        # Check if it is the end word
        if words_found[word_id] == end_word:
            return True
        else:
            # Add its children to the pile
            children = get_children(
                current_position=current_position,
                position_to_word_id=position_to_word_id
            )
            for child in children:
                pile.append(child)

    return False


def is_in_english_words(word: str):
    """
    Indicates whether a word belongs to the english words dictionary or not.

    Parameters
    ----------
    word : str
        Word to check.

    Returns
    -------
    bool
        True if the word is in the dictionary, False otherwise.
    """

    return dichotomy(word, ENGLISH_WORDS_DICTS["280k"]) is not None


def count_different_letters(word1: str, word2: str) -> int:
    """
    Count the number of different letters between two words.

    Parameters
    ----------
    word1 : str
        First word.
    word2 : str
        Second word.

    Returns
    -------
    int
        Number of different letters.
    """

    # Initialise the number of different letters
    nb_different_letters = 0
    used_letters = [False] * len(word2)

    # Iterate over the letters of the first word
    for letter in word1:
        valid_letter_bool = False
        for i, check_letter in enumerate(word2):
            if check_letter == letter and used_letters[i] is False:
                used_letters[i] = True
                valid_letter_bool = True
                break
        if valid_letter_bool is False:
            nb_different_letters += 1

    return nb_different_letters


def compute_similarity_score(word1: str, word2: str) -> int:
    res = count_different_letters(word1, word2)
    res += abs(len(word2) - len(word1))
    score = MAX_NB_LETTERS - res
    if score < 0:
        score = 0
    return score


def level_has_saved_data(level_dict: dict):
    """
    Return True if the level dict has saved data and False otherwise.

    Parameters
    ----------
    level_dict : dict
        Dictionary containing the level information.

    Returns
    -------
    bool
        True if the level dict has saved data and False otherwise.
    """

    return "words_found" in level_dict and "position_to_word_id" in level_dict and "current_position" in level_dict


def is_valid(new_word: str, current_word: str, skip_in_english_words: bool = False) -> bool:
    """
    Determine whether a word is valid or not to be submitted.

    Parameters
    ----------
    new_word : str
        New word to check.
    current_word : str
        Current word.
    skip_in_english_words : bool = False
        If True, a word doesn't need to be in any dictionary to be valid (i.e., in_english_words() is not called here).

    Returns
    -------
    bool
        True if the word is valid, False otherwise.
    """

    # Limit the number of letters
    if len(new_word) > MAX_NB_LETTERS:
        return False

    # Check if the new word derives from the current word
    if len(new_word) - len(current_word) == 0:
        # Shuffle and change one letter case
        if count_different_letters(new_word, current_word) <= 1:
            derive_bool = True
        else:
            derive_bool = False
    elif len(new_word) - len(current_word) == 1:
        # New letter addition case
        if count_different_letters(new_word, current_word) <= 1:
            derive_bool = True
        else:
            derive_bool = False
    elif len(new_word) - len(current_word) == -1:
        # Letter deletion case
        if count_different_letters(new_word, current_word) == 0:
            derive_bool = True
        else:
            derive_bool = False
    else:
        derive_bool = False

    # Check if the new word is in the english dictionary
    if skip_in_english_words:
        english_words_bool = True
    else:
        english_words_bool = is_in_english_words(new_word)

    # Check if the new word verifies both conditions
    valid_bool = derive_bool and english_words_bool

    return valid_bool


def find_all_next_words(current_word: str, end_word: str, english_words: list):
    next_words = []
    for word in english_words:
        if is_valid(word, current_word, skip_in_english_words=True):
            next_words.append(word)

    # Add the end word if not in english dictionnary but still valid
    if is_valid(end_word, current_word, skip_in_english_words=True) and end_word not in next_words:
        next_words.append(end_word)

    return next_words


def convert_position_to_wordlist(position: str, position_to_word_id, words_found):
    wordlist = []
    for i in range(1, len(position) + 1):
        word = words_found[position_to_word_id[position[:i]]]
        wordlist.append(word)
    return wordlist


def find_solutions(start_word: str, end_word: str, english_words: list = ENGLISH_WORDS_DICTS["280k"], time_out=None):
    """
    Find solutions for the given start and end words by using a score based on proximity to the end word.

    Parameters
    ----------
    start_word : str
        Start word.
    end_word : str
        End word.
    english_words : list, optional
        Database to use to create the path, by default ENGLISH_WORDS_DICTS["280k"]

    Returns
    -------
    list
        Path between the two words.
    """

    start_position = (0,)
    position_to_word_id = {start_position: 0}
    words_found = [start_word]
    pile = {}

    for i in range(len(end_word) + 1):
        pile[i] = []

    pile[0].append(start_position)

    not_found = True
    start_timer = time.time()

    while not_found:

        current_position = None
        for i in sorted(pile.keys(), reverse=True):
            if len(pile[i]) > 0:
                # print(i)
                current_position = pile[i].pop(0)
                break

        if current_position is None:
            return None

        current_word = words_found[position_to_word_id[current_position]]
        next_words = find_all_next_words(
            current_word=current_word, end_word=end_word, english_words=english_words)
        new_word_id = 0

        for word in next_words:
            if time_out is not None:
                if time.time() - start_timer > time_out:
                    return None
            if word not in words_found or word == end_word:
                similarity_score = compute_similarity_score(word, end_word)
                new_position = current_position + (new_word_id,)
                position_to_word_id[new_position] = len(words_found)
                words_found.append(word)
                new_word_id += 1
                if word == end_word:
                    not_found = False
                    final_position = new_position
                    print(convert_position_to_wordlist(
                        final_position, position_to_word_id, words_found))
                else:
                    pile_id = similarity_score - len(new_position)
                    # print(pile_id)
                    if pile_id in pile:
                        pile[pile_id].append(new_position)
                    else:
                        pile[pile_id] = [new_position]

    solution = []
    for i in range(1, len(final_position) + 1):
        word = words_found[position_to_word_id[final_position[:i]]]
        solution.append(word)

    return solution


def fill_daily_games_with_solutions():
    """
    Fill all the empty lines of the daily games json with the solutions.
    """
    DAILY_DICT = load_json_file(PATH_RESOURCES + "daily_games.json")
    for date in DAILY_DICT:
        start_word = DAILY_DICT[date]["start_word"]
        end_word = DAILY_DICT[date]["end_word"]
        if "simplest_solution" not in date:
            for resolution in ENGLISH_WORDS_DICTS:
                solution = find_solutions(
                    start_word=start_word,
                    end_word=end_word,
                    english_words=ENGLISH_WORDS_DICTS[resolution])
                if solution is not None:
                    DAILY_DICT[date]["simplest_solution"] = solution
                    break
        if "best_solution" not in date:
            if resolution != "280k":
                solution = find_solutions(
                    start_word=start_word,
                    end_word=end_word,
                    english_words=ENGLISH_WORDS_DICTS["280k"])
            DAILY_DICT[date]["best_solution"] = solution
        save_json_file(PATH_RESOURCES + "daily_games.json", DAILY_DICT)


def fill_gameplay_dict_with_solutions():
    """
    Fill all the empty lines of the gameplay dict with the solutions.
    """
    for act in GAMEPLAY_DICT:
        for level in GAMEPLAY_DICT[act]:
            if level == "name":
                # GAMEPLAY_DICT[act] has one key called "name" to store the act's title. All other keys are the ids of the levels in the act.
                continue
            start_word = GAMEPLAY_DICT[act][level]["start_word"]
            end_word = GAMEPLAY_DICT[act][level]["end_word"]
            for resolution in DICT_ID_LIST:
                if resolution not in GAMEPLAY_DICT[act][level]:
                    print(resolution)
                    solution = find_solutions(
                        start_word=start_word,
                        end_word=end_word,
                        english_words=ENGLISH_WORDS_DICTS[resolution])
                    if solution is not None:
                        GAMEPLAY_DICT[act][level][resolution] = len(
                            solution)
                    else:
                        GAMEPLAY_DICT[act][level][resolution] = None

            save_json_file(PATH_GAMEPLAY, GAMEPLAY_DICT)

#############
### Class ###
#############


class AdContainer():

    nb_max_reload = 3

    def __init__(self) -> None:
        self.current_ad = None
        self.load_ad()
        print("Ad container initialization")

    def watch_ad(self, ad_callback: Callable, ad_fail: Callable = lambda: 1 + 1):
        reload_id = 0
        if ANDROID_MODE:
            self.current_ad: RewardedAd
            print("try to show ads")
            print("Ad state:", self.current_ad.is_loaded())

            # Reload ads if fail
            while not self.current_ad.is_loaded() and reload_id < self.nb_max_reload:
                self.current_ad = None
                self.load_ad()
                time.sleep(0.3)
                reload_id += 1
                print("Reload ad", reload_id)

            # Check if ads is finally loaded
            if not self.current_ad.is_loaded():
                ad_fail()
                self.current_ad = None
                self.load_ad()
            else:
                self.current_ad.on_reward = ad_callback
                self.current_ad.show()
        elif IOS_MODE:
            #self.current_ad.RewardedView()
            self.current_ad.InterstitialView()
            ad_callback()
        else:
            print("No ads to show outside mobile mode")
            ad_callback()

    def load_ad(self):
        print("try to load ad")
        if ANDROID_MODE:
            self.current_ad = RewardedAd(
                # REWARD_INTERSTITIAL,
                # TestID.REWARD,
                REWARD_AD,
                on_reward=None)
        elif IOS_MODE:
            # self.current_ad = autoclass("adRewarded").alloc().init()
            self.current_ad = autoclass("adInterstitial").alloc().init()
        else:
            self.current_ad = None


AD_CONTAINER = AdContainer()


class Game():
    """
    Class to manage all actions and variables during a game of Linconym.
    Its member variables represent a tree of words, the root of which is the start word of the game.
    Its member variables also include a cursor "pointing" to one node in particular: new words submitted by the user
    may be added as children of the node "pointed to" by this cursor if they are valid successors.
    """

    def __init__(
            self,
            start_word: str,
            end_word: str,
            current_position: str = None,
            words_found: list = None,
            position_to_word_id: dict = None,
            quest_word: str = None) -> None:
        """
        Create a game instance.

        Parameters
        ----------
        start_word : str
            _description_
        end_word : str
            _description_
        current_position : str, optional (default is None)
            _description_
        words_found : list, optional (default is None)
            _description_
        position_to_word_id : dict, optional (default is None)
            _description_
        quest_word : str, optional (default is None)
            _description_

        Returns
        -------
        Game
            Instance of the game class.
        """

        self.start_word: str = start_word
        self.end_word: str = end_word
        self.quest_word: str = quest_word
        # Positions are strings of comma-separated integers which indicate a path in the nodes
        if current_position is not None:
            self.current_position = current_position
        else:
            self.current_position: str = "0"
        # A dictionary to map a (str) position to the index of its word in the words_found list[str]
        if position_to_word_id is not None:
            self.position_to_word_id = position_to_word_id
        else:
            self.position_to_word_id = {self.current_position: 0}
        if words_found is not None:
            self.words_found = words_found
        else:
            self.words_found: list[str] = [start_word]
        self.current_word: str = self.words_found[self.position_to_word_id[self.current_position]]

    def get_word(self, position: str) -> str:
        """
        Get the word at given position.

        Parameters
        ----------
        position : str
            Position to use.

        Returns
        -------
        str
            Word at given position.
        """

        return self.words_found[self.position_to_word_id[position]]

    def get_word_path(self, position: str) -> list[str]:
        """
        Get a list of the words forming the path to the given position.

        Parameters
        ----------
        position : str
            Position to use.

        Returns
        -------
        list[str]
            List of words leading to given position.
        """

        word_path: list[str] = []
        splitted_position = position.split(",")
        for i in range(len(splitted_position)):
            splitted_previous_pos: str = splitted_position[:(i + 1)]
            previous_pos = splitted_previous_pos[0]
            for j in range(1, len(splitted_previous_pos)):
                previous_pos += "," + splitted_previous_pos[j]
            word_path += [self.get_word(previous_pos)]

        return word_path

    def get_next_words(self, position: str) -> list[str]:
        """
        Get the list of next words currently found.

        Parameters
        ----------
        position : str
            Current position.

        Returns
        -------
        list[str]
            List of the next words.
        """

        # Initialise the number of next words
        next_words = []

        # Iterate over all stored positions
        for key in self.position_to_word_id:
            if len(key.split(",")) == len(position.split(",")) + 1:
                if key[:len(position)] == position:
                    next_words.append(self.words_found[
                        self.position_to_word_id[key]])

        return next_words

    def get_nb_next_words(self, position: str) -> int:
        """
        Get the number of words deriving directly from the given position.
        In tree jargon, get the number of children of the node corresponding to the input position.

        Parameters
        ----------
        position : str
            Position to use.

        Returns
        -------
        int
            Number of next words.
        """

        # Initialise the number of next words
        nb_next_words = 0

        # Iterate over all stored positions
        for key in self.position_to_word_id:
            if len(key.split(",")) == len(position.split(",")) + 1:
                if key[:len(position)] == position:
                    nb_next_words += 1

        return nb_next_words

    def change_position(self, new_position: str) -> None:
        """
        Change the position of the cursor from one word (node) to another.

        Parameters
        ----------
        new_position : str
            New position to set.
        """

        self.current_position = new_position
        self.current_word = self.get_word(self.current_position)

    def is_valid_and_new_in_path(self, new_word: str, skip_dictionary_check: bool = False) -> bool:
        """
        Checks whether a new word is absent from the path leading to the current word and is a valid successor to the current word.

        Parameters
        ----------
        new_word: str
            New word to be checked.
        skip_dictionary_check: bool = False
            If True, new_word can be valid even if it isn't in any dictionary.

        Returns
        -------
        bool
            True if new_word isn't in the path leading to the current word and is valid, False otherwise.
        """

        word_is_valid: bool = is_valid(
            new_word, self.current_word, skip_dictionary_check)
        word_is_new_in_path: bool = not (
            new_word in self.get_word_path(self.current_position))

        word_is_not_in_children = not (
            new_word in self.get_next_words(self.current_position)
        )
        return word_is_valid and word_is_new_in_path and word_is_not_in_children

    def submit_word(self, new_word: str) -> None:
        """
        Add a new word to the history if it is valid.

        Parameters
        ----------
        new_word : str
            New word to verify and add.
        """

        if self.is_valid_and_new_in_path(new_word):

            # Compute the new position
            new_word_id = self.get_nb_next_words(self.current_position)
            new_position = self.current_position + "," + str(new_word_id)

            # Add the word to the list of words found
            self.position_to_word_id[new_position] = len(self.words_found)
            self.words_found.append(new_word)

            # Switch to the new position
            self.change_position(new_position)
        else:
            print("Word not valid")

    def delete_current_word(self):
        """
        Delete the current word.

        Warning
        -------
        Do not use this function if the current word has children.
        """

        # Remove word from position to word_id
        self.position_to_word_id.pop(self.current_position)

        # Get the position of the parent
        new_position = get_parent_position(self.current_position)

        # Move to the position of the parent
        self.change_position(new_position)

    def get_nb_words_2nd_star(self) -> int:
        """
        Returns
        -------
        int
            Maximum number of words in a solution to get the level's second star
        """
        # This is supposed to be an abstract method. It'll be overridden by Game's subclasses.

        return 0

    def get_nb_words_3rd_star(self) -> int:
        """
        Returns
        -------
        int
            Maximum number of words in a solution to get the level's third star
        """
        # This is supposed to be an abstract method. It'll be overridden by Game's subclasses.

        return 0

    def get_nb_stars(self, nb_words_found: int) -> int:
        """
        Computes how many stars are awarded for a given solution.

        Parameters
        ----------
        nb_words_found: int
            Length (in words) of one of the level's solutions.

        Returns
        -------
        int
            Number of stars awarded for finding said solution.
        """

        nb_stars: int = 1  # first star is awarded for finishing the level
        if (nb_words_found <= self.get_nb_words_2nd_star()):
            nb_stars += 1
            if (nb_words_found <= self.get_nb_words_3rd_star()):
                nb_stars += 1
        return nb_stars

    def get_xp_fraction(self, nb_words_found: int) -> float:
        """
        Computes the fraction of XP awarded for a given solution.

        Parameters
        ----------
        nb_words_found: int
            Length (in words) of one of the level's solutions.

        Returns
        -------
        float
            Fraction of XP awarded for finding said solution.
        """
        # This is supposed to be an abstract method. It'll be overridden by Game's subclasses.

        return 0.0

    def award_stars_xp(self) -> None:
        """
        Saves the number of stars and the amount of XP earned in this level in the user's data, and increases the user's XP in their profile accordingly.
        """
        # This is supposed to be an abstract method. It'll be overridden by Game's subclasses.

        return

    def on_level_completed(self):
        pass

    def get_hint(self) -> str:
        """
        Give a hint for the next word base on what has already been completed.
        """

        # Iterate over the different dictionaries
        for resolution in DICT_ID_LIST[1:]:
            # Remove the words founds from the dict
            current_words_dict = ENGLISH_WORDS_DICTS[resolution].copy()
            for word in self.words_found:
                if word in current_words_dict:
                    current_words_dict.remove(word)

            # Find solution
            solution = find_solutions(self.current_word, self.end_word,
                                      current_words_dict, time_out=10)
            if solution is not None:
                return solution[1]

        return None


class ClassicGame(Game):
    def __init__(
            self,
            act_id: str,
            lvl_id: str,
            current_position: str = None,
            position_to_word_id: dict = None,
            words_found: list = None,
            quest_word: str = None) -> None:
        self.act_id: str = act_id
        self.lvl_id: str = lvl_id

        # Load level data from GAMEPLAY_DICT
        self.sol_data: dict = None
        if ((self.act_id in GAMEPLAY_DICT) and (self.lvl_id in GAMEPLAY_DICT[self.act_id])):
            self.sol_data = GAMEPLAY_DICT[self.act_id][self.lvl_id]
        else:
            raise ValueError(
                "Level data absent from gameplay dict:", act_id + "," + lvl_id)

        # Load first possible solution length and 280k solution length from GAMEPLAY_DICT
        has_sol: bool = False
        self.first_sol_dict_id: str = ""
        self.nb_words_first_sol: int = 0
        self.nb_words_280k_sol: int = 0

        for dict_id in DICT_ID_LIST:
            if (not (self.sol_data[dict_id] is None)):
                self.first_sol_dict_id = dict_id
                has_sol = True
                break

        if (not (has_sol)):
            raise ValueError(
                "The solution dict does not contain any valid solution:", self.sol_data)
        else:
            self.nb_words_first_sol = self.sol_data[self.first_sol_dict_id]
            self.nb_words_280k_sol = self.sol_data[DICT_ID_LIST[-1]]

        super().__init__(
            start_word=self.sol_data["start_word"],
            end_word=self.sol_data["end_word"],
            current_position=current_position,
            position_to_word_id=position_to_word_id,
            words_found=words_found,
            quest_word=quest_word
        )

    def get_nb_words_2nd_star(self) -> int:
        """
        Returns
        -------
        int
            Maximum number of words in a solution to get the level's second star
        """

        nb_words_2nd_star: int = 0
        if (self.first_sol_dict_id == DICT_ID_LIST[0]):
            # In easy levels (those which have a solution in the 10k dict), the second star is awarded for doing as well as the 10k dict + a margin (25%)
            nb_words_2nd_star = int(1.25 * self.nb_words_first_sol)
        else:
            # In harder levels (no solution in the 10k dict), the second star is awarded for doing as well as the first solution dict + a wider margin (30%)
            nb_words_2nd_star = int(1.30 * self.nb_words_first_sol)
        return nb_words_2nd_star

    def get_nb_words_3rd_star(self) -> int:
        """
        Returns
        -------
        int
            Maximum number of words in a solution to get the level's third star
        """

        nb_words_3rd_star: int = 0
        if (self.first_sol_dict_id == DICT_ID_LIST[0]):
            # In easy levels (those which have a solution in the 10k dict), the third star is awarded for doing as well as the 10k dict
            nb_words_3rd_star = self.nb_words_first_sol
        else:
            # In harder levels (no solution in the 10k dict), the third star is awarded for doing as well as the first solution dict + a small margin (10%)
            nb_words_3rd_star = int(1.10 * self.nb_words_first_sol)
        return nb_words_3rd_star

    def get_xp_fraction(self, nb_words_found: int) -> float:
        """
        Computes the fraction of XP awarded for a given solution.

        Parameters
        ----------
        nb_words_found: int
            Length (in words) of one of the level's solutions.

        Returns
        -------
        float
            Fraction of XP awarded for finding said solution.
        """

        # There's probably a smoother way to compute this, but that's a problem for later
        xp_fraction: float = self.nb_words_280k_sol / nb_words_found
        if (xp_fraction > 1):
            xp_fraction = 1.0
        return xp_fraction

    def award_stars_xp(self, solution_found) -> None:
        """
        Saves the number of stars and the amount of XP earned in this level in the user's data, and increases the user's XP in their profile accordingly.
        """

        # Solution found by the user
        solution_found: list[str] = self.get_word_path(
            self.current_position)

        # Stars
        nb_words_found: int = len(solution_found)
        self.nb_stars: int = self.get_nb_stars(nb_words_found)

        # Awards
        self.xp_earned: int = 0
        self.lincoins_earned: int = 0

        # xp: get a percentage of a certain constant amount depending on the solution's quality...
        xp_fraction: float = self.get_xp_fraction(nb_words_found)
        # ... and get a bonus for passing through the quest word
        quest_word_done: bool = (not (self.quest_word is None) and (
            self.quest_word in solution_found))

        # check that the current act has save data
        if (not (self.act_id in USER_DATA.classic_mode)):
            USER_DATA.classic_mode[self.act_id] = {}

        # check that current level has save data
        if (not (self.lvl_id in USER_DATA.classic_mode[self.act_id])):
            USER_DATA.classic_mode[self.act_id][self.lvl_id] = {}

        # recover previous best number of words
        nb_words_previous_best: int = 0
        previous_exists: bool = USER_DATA.classic_mode[self.act_id][self.lvl_id]["nb_stars"] > 0
        previous_best_exists: bool = False
        if (NB_WORDS_KEY in USER_DATA.classic_mode[self.act_id][self.lvl_id]):
            nb_words_previous_best = USER_DATA.classic_mode[self.act_id][self.lvl_id][NB_WORDS_KEY]
            previous_best_exists = True

        # If the user did better than last time, overwrite everything
        if ((nb_words_found < nb_words_previous_best) or not (previous_best_exists)):
            # save best number of words
            USER_DATA.classic_mode[self.act_id][self.lvl_id][NB_WORDS_KEY] = nb_words_found
            # save stars
            USER_DATA.classic_mode[self.act_id][self.lvl_id][STARS_KEY] = self.nb_stars
            # recover previous xp fraction and stars
            previous_xp_fraction: float = 0.0
            previous_nb_stars: int = 0
            if (previous_best_exists):
                previous_xp_fraction = self.get_xp_fraction(
                    nb_words_previous_best)
                previous_nb_stars = self.get_nb_stars(nb_words_previous_best)
            # award newly acquired xp
            self.xp_earned = int(round(
                (xp_fraction - previous_xp_fraction) * XP_PER_CLASSIC_PUZZLE, 0))
            USER_DATA.user_profile[XP_KEY] += self.xp_earned
            # Award newly acquired lincoins
            lincoins_earned_before = NB_LINCOINS_PER_STAR_CLASSIC_DICT[previous_nb_stars]
            lincoins_now = NB_LINCOINS_PER_STAR_CLASSIC_DICT[self.nb_stars]
            self.lincoins_earned = lincoins_now - lincoins_earned_before
            USER_DATA.user_profile["lincoins"] += self.lincoins_earned
            USER_DATA.user_profile["cumulated_lincoins"] += self.lincoins_earned

        # Set the number of Linclues won in chests
        self.linclues_earned = 0
        if "chest" in GAMEPLAY_DICT[self.act_id][self.lvl_id] and GAMEPLAY_DICT[self.act_id][self.lvl_id]["chest"]:
            # If the user has not already opened the chest
            if not previous_exists:
                self.linclues_earned = 3
                USER_DATA.user_profile["linclues"] += 3
                USER_DATA.user_profile["cumulated_linclues"] += 3
                USER_DATA.save_changes()

        # If the user passed through the quest word (if any) for the first time, award bonus xp
        # award_quest_word_xp: bool = False
        # if (QUEST_WORD_KEY in USER_DATA.classic_mode[self.act_id][self.lvl_id]):
        #     already_did_quest_word: bool = USER_DATA.classic_mode[
        #         self.act_id][self.lvl_id][QUEST_WORD_KEY]
        #     award_quest_word_xp = quest_word_done and not (
        #         already_did_quest_word)
        #     USER_DATA.classic_mode[self.act_id][self.lvl_id][QUEST_WORD_KEY] = already_did_quest_word or quest_word_done
        # else:
        #     award_quest_word_xp = quest_word_done
        #     USER_DATA.classic_mode[self.act_id][self.lvl_id][QUEST_WORD_KEY] = quest_word_done
        # if (award_quest_word_xp):
        #     USER_DATA.user_profile[XP_KEY] += XP_PER_CLASSIC_PUZZLE

        # Save changes
        USER_DATA.save_changes()

    def unlock_next_level(self):
        """
        Unlock the next level in same act or in the next act.
        """

        # Determine if there is other levels to unlock in the same act
        next_lvl_id = str(int(self.lvl_id) + 1)
        if next_lvl_id in GAMEPLAY_DICT[self.act_id] and next_lvl_id not in USER_DATA.classic_mode[self.act_id]:
            # Unlock the next level in the same act
            USER_DATA.classic_mode[self.act_id][next_lvl_id] = {"nb_stars": 0}

        USER_DATA.save_changes()

    def on_level_completed(self):
        solution_found: list[str] = self.get_word_path(
            self.current_position)
        nb_words_found: int = len(solution_found)

        # Save the xp and stars
        self.award_stars_xp(solution_found)

        # Unlock the next level
        self.unlock_next_level()

        # Compute the progression for level up
        previous_level, previous_level_progress = compute_progression(
            USER_DATA.user_profile[XP_KEY] - self.xp_earned)

        current_level, current_level_progress = compute_progression(
            USER_DATA.user_profile[XP_KEY])

        if previous_level < current_level:
            has_level_up = True
            previous_level_progress = 0
        else:
            has_level_up = False

        # Update level in saved data
        USER_DATA.user_profile["level"] = current_level
        USER_DATA.save_changes()

        # Create a dict to return the data
        end_level_dict = {
            "stars": self.nb_stars,
            "nb_words": nb_words_found,
            "xp_earned": self.xp_earned,
            "lincoins_earned": self.lincoins_earned,
            "linclues_earned": self.linclues_earned,
            "has_level_up": has_level_up,
            "previous_level_progress": previous_level_progress,
            "current_level_progress": current_level_progress
        }

        return end_level_dict


class LegendGame(Game):
    def __init__(
            self,
            act_id: str,
            lvl_id: str,
            current_position: str = None,
            position_to_word_id: dict = None,
            words_found: list = None,
            quest_word: str = None) -> None:
        self.act_id: str = act_id
        self.lvl_id: str = lvl_id

        # Load level data from GAMEPLAY_LEGEND_DICT
        self.sol_data: dict = None
        if ((self.act_id in GAMEPLAY_LEGEND_DICT) and (self.lvl_id in GAMEPLAY_LEGEND_DICT[self.act_id])):
            self.sol_data = GAMEPLAY_LEGEND_DICT[self.act_id][self.lvl_id]
        else:
            raise ValueError(
                "Level data absent from gameplay dict:", act_id + "," + lvl_id)

        # Load first possible solution length and 280k solution length from GAMEPLAY_LEGEND_DICT
        has_sol: bool = False
        self.first_sol_dict_id: str = ""
        self.nb_words_first_sol: int = 0
        self.nb_words_280k_sol: int = 0

        for dict_id in DICT_ID_LIST:
            if (not (self.sol_data[dict_id] is None)):
                self.first_sol_dict_id = dict_id
                has_sol = True
                break

        if (not (has_sol)):
            raise ValueError(
                "The solution dict does not contain any valid solution:", self.sol_data)
        else:
            self.nb_words_first_sol = self.sol_data[self.first_sol_dict_id]
            self.nb_words_280k_sol = self.sol_data[DICT_ID_LIST[-1]]

        super().__init__(
            start_word=self.sol_data["start_word"],
            end_word=self.sol_data["end_word"],
            current_position=current_position,
            position_to_word_id=position_to_word_id,
            words_found=words_found,
            quest_word=quest_word
        )

    def get_nb_words_2nd_star(self) -> int:
        """
        Returns
        -------
        int
            Maximum number of words in a solution to get the level's second star
        """

        nb_words_2nd_star: int = 0
        if (self.first_sol_dict_id == DICT_ID_LIST[0]):
            # In easy levels (those which have a solution in the 10k dict), the second star is awarded for doing as well as the 10k dict + a margin (25%)
            nb_words_2nd_star = int(1.25 * self.nb_words_first_sol)
        else:
            # In harder levels (no solution in the 10k dict), the second star is awarded for doing as well as the first solution dict + a wider margin (30%)
            nb_words_2nd_star = int(1.30 * self.nb_words_first_sol)
        return nb_words_2nd_star

    def get_nb_words_3rd_star(self) -> int:
        """
        Returns
        -------
        int
            Maximum number of words in a solution to get the level's third star
        """

        nb_words_3rd_star: int = 0
        if (self.first_sol_dict_id == DICT_ID_LIST[0]):
            # In easy levels (those which have a solution in the 10k dict), the third star is awarded for doing as well as the 10k dict
            nb_words_3rd_star = self.nb_words_first_sol
        else:
            # In harder levels (no solution in the 10k dict), the third star is awarded for doing as well as the first solution dict + a small margin (10%)
            nb_words_3rd_star = int(1.10 * self.nb_words_first_sol)
        return nb_words_3rd_star

    def get_xp_fraction(self, nb_words_found: int) -> float:
        """
        Computes the fraction of XP awarded for a given solution.

        Parameters
        ----------
        nb_words_found: int
            Length (in words) of one of the level's solutions.

        Returns
        -------
        float
            Fraction of XP awarded for finding said solution.
        """

        # There's probably a smoother way to compute this, but that's a problem for later
        xp_fraction: float = self.nb_words_280k_sol / nb_words_found
        if (xp_fraction > 1):
            xp_fraction = 1.0
        return xp_fraction

    def award_stars_xp(self, solution_found) -> None:
        """
        Saves the number of stars and the amount of XP earned in this level in the user's data, and increases the user's XP in their profile accordingly.
        """

        # Solution found by the user
        solution_found: list[str] = self.get_word_path(
            self.current_position)

        # Stars
        nb_words_found: int = len(solution_found)
        self.nb_stars: int = self.get_nb_stars(nb_words_found)

        # Awards
        self.xp_earned: int = 0
        self.lincoins_earned: int = 0

        # xp: get a percentage of a certain constant amount depending on the solution's quality...
        xp_fraction: float = self.get_xp_fraction(nb_words_found)
        # ... and get a bonus for passing through the quest word
        quest_word_done: bool = (not (self.quest_word is None) and (
            self.quest_word in solution_found))

        # check that the current act has save data
        if (not (self.act_id in USER_DATA.legend_mode)):
            USER_DATA.legend_mode[self.act_id] = {}

        # check that current level has save data
        if (not (self.lvl_id in USER_DATA.legend_mode[self.act_id])):
            USER_DATA.legend_mode[self.act_id][self.lvl_id] = {}

        # recover previous best number of words
        nb_words_previous_best: int = 0
        previous_exists: bool = USER_DATA.legend_mode[self.act_id][self.lvl_id]["nb_stars"] > 0
        previous_best_exists: bool = False
        if (NB_WORDS_KEY in USER_DATA.legend_mode[self.act_id][self.lvl_id]):
            nb_words_previous_best = USER_DATA.legend_mode[self.act_id][self.lvl_id][NB_WORDS_KEY]
            previous_best_exists = True

        # If the user did better than last time, overwrite everything
        if ((nb_words_found < nb_words_previous_best) or not (previous_best_exists)):
            # save best number of words
            USER_DATA.legend_mode[self.act_id][self.lvl_id][NB_WORDS_KEY] = nb_words_found
            # save stars
            USER_DATA.legend_mode[self.act_id][self.lvl_id][STARS_KEY] = self.nb_stars
            # recover previous xp fraction and stars
            previous_xp_fraction: float = 0.0
            previous_nb_stars: int = 0
            if (previous_best_exists):
                previous_xp_fraction = self.get_xp_fraction(
                    nb_words_previous_best)
                previous_nb_stars = self.get_nb_stars(nb_words_previous_best)
            # award newly acquired xp
            self.xp_earned = int(round(
                (xp_fraction - previous_xp_fraction) * XP_PER_LEGEND_PUZZLE, 0))
            USER_DATA.user_profile[XP_KEY] += self.xp_earned
            # Award newly acquired lincoins
            lincoins_earned_before = NB_LINCOINS_PER_STAR_LEGEND_DICT[previous_nb_stars]
            lincoins_now = NB_LINCOINS_PER_STAR_LEGEND_DICT[self.nb_stars]
            self.lincoins_earned = lincoins_now - lincoins_earned_before
            USER_DATA.user_profile["lincoins"] += self.lincoins_earned
            USER_DATA.user_profile["cumulated_lincoins"] += self.lincoins_earned

        # Set the number of Linclues won in chests
        self.linclues_earned = 0
        if "chest" in GAMEPLAY_LEGEND_DICT[self.act_id][self.lvl_id] and GAMEPLAY_LEGEND_DICT[self.act_id][self.lvl_id]["chest"]:
            # If the user has not already opened the chest
            if not previous_exists:
                self.linclues_earned = 3
                USER_DATA.user_profile["linclues"] += 3
                USER_DATA.user_profile["cumulated_linclues"] += 3
                USER_DATA.save_changes()

        # If the user passed through the quest word (if any) for the first time, award bonus xp
        # award_quest_word_xp: bool = False
        # if (QUEST_WORD_KEY in USER_DATA.legend_mode[self.act_id][self.lvl_id]):
        #     already_did_quest_word: bool = USER_DATA.legend_mode[
        #         self.act_id][self.lvl_id][QUEST_WORD_KEY]
        #     award_quest_word_xp = quest_word_done and not (
        #         already_did_quest_word)
        #     USER_DATA.legend_mode[self.act_id][self.lvl_id][QUEST_WORD_KEY] = already_did_quest_word or quest_word_done
        # else:
        #     award_quest_word_xp = quest_word_done
        #     USER_DATA.legend_mode[self.act_id][self.lvl_id][QUEST_WORD_KEY] = quest_word_done
        # if (award_quest_word_xp):
        #     USER_DATA.user_profile[XP_KEY] += XP_PER_LEGEND_PUZZLE

        # Save changes
        USER_DATA.save_changes()

    def unlock_next_level(self):
        """
        Unlock the next level in same act or in the next act.
        """

        # Determine if there is other levels to unlock in the same act
        next_lvl_id = str(int(self.lvl_id) + 1)
        if next_lvl_id in GAMEPLAY_LEGEND_DICT[self.act_id] and next_lvl_id not in USER_DATA.legend_mode[self.act_id]:
            # Unlock the next level in the same act
            USER_DATA.legend_mode[self.act_id][next_lvl_id] = {"nb_stars": 0}

        USER_DATA.save_changes()

    def on_level_completed(self):
        solution_found: list[str] = self.get_word_path(
            self.current_position)
        nb_words_found: int = len(solution_found)

        # Save the xp and stars
        self.award_stars_xp(solution_found)

        # Unlock the next level
        self.unlock_next_level()

        # Compute the progression for level up
        previous_level, previous_level_progress = compute_progression(
            USER_DATA.user_profile[XP_KEY] - self.xp_earned)

        current_level, current_level_progress = compute_progression(
            USER_DATA.user_profile[XP_KEY])

        if previous_level < current_level:
            has_level_up = True
            previous_level_progress = 0
        else:
            has_level_up = False

        # Update level in saved data
        USER_DATA.user_profile["level"] = current_level
        USER_DATA.save_changes()

        # Create a dict to return the data
        end_level_dict = {
            "stars": self.nb_stars,
            "nb_words": nb_words_found,
            "xp_earned": self.xp_earned,
            "lincoins_earned": self.lincoins_earned,
            "linclues_earned": self.linclues_earned,
            "has_level_up": has_level_up,
            "previous_level_progress": previous_level_progress,
            "current_level_progress": current_level_progress
        }

        return end_level_dict


if __name__ == "__main__":

    # To use to complete the solution
    fill_gameplay_dict_with_solutions()

    # game = Game(
    #     start_word="link",
    #     end_word="pink",
    #     current_position="0",
    #     words_found=["link", "like"],
    #     position_to_word_id={"0": 0, "0,0": 1}
    # )

    # game.submit_word("pink")

    # fill_daily_games_with_solutions()
    # print(is_valid("brain", "crane"))
    find_solutions("luxury", "chic", ENGLISH_WORDS_DICTS["10k"])
    pass
