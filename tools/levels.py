"""
Module to store the functions related to experience, levels and status.
"""

###############
### Imports ###
###############


from tools.constants import (
    XP_PER_LEVEL,
    USER_STATUS_DICT
)

#################
### Functions ###
#################


def convert_rank_name_to_int(rank_name: str):
    """
    Convert the string id of a rank to a int id to perform computations.

    Parameters
    ----------
    rank_name : str
        Name of the rank

    Returns
    -------
    int
        Int id of the rank.
    """

    # Extract the list of ranks
    rank_list = list(USER_STATUS_DICT.keys())

    # Scan it to find the int id
    for i, current_rank_name in enumerate(rank_list):
        if current_rank_name == rank_name:
            return i

    # Raise error if the rank is not found
    return ValueError("Rank not found.")


def get_rank(level: int):
    """
    Compute the rank corresponding to the given level.

    Parameters
    ----------
    level : int
        Given level for which to compute the rank.

    Returns
    -------
    str
        Name of the rank associated to the level.
    """

    # Iterate over the ranks to find the corresponding one
    for rank_name in USER_STATUS_DICT:
        begin = USER_STATUS_DICT[rank_name]["begin"]
        end = USER_STATUS_DICT[rank_name]["end"]
        if begin <= level <= end:
            return rank_name

    # Raise error if the rank is not found
    return ValueError("Rank not found.")


def get_level(total_xp: int, get_remaining_xp: bool = False):
    """
    Compute the level given the amount of experience.

    Parameters
    ----------
    total_xp : int
        Amount of experience.

    Returns
    -------
    int
        Level.
    """

    # Allocate a variable for the level
    level = 1

    # Convert xp to levels progressively
    while total_xp >= 0:
        current_rank = get_rank(level)
        current_rank_id = convert_rank_name_to_int(current_rank)
        remaining_xp = total_xp
        total_xp -= (1 + 2 * current_rank_id) * XP_PER_LEVEL
        if total_xp >= 0:
            level += 1

    # Return the appropriate values
    if get_remaining_xp is False:
        return level
    else:
        return level, remaining_xp


if __name__ == "__main__":
    print(get_level(401, get_remaining_xp=True))
