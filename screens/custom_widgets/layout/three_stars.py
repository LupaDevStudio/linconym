"""
Module to create three stars with a certain filling ratio
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    NumericProperty,
    ListProperty,
    BooleanProperty
)

#############
### Class ###
#############


class ThreeStars(RelativeLayout):
    """
    Class to create a widget with three stars that can be turn on and off.
    """

    star_one_color = ListProperty([0.5, 0.5, 0.5, 1.])
    star_two_color = ListProperty([0.5, 0.5, 0.5, 1.])
    star_three_color = ListProperty([0.5, 0.5, 0.5, 1.])
    star_one_contour_opacity = NumericProperty(1)
    star_two_contour_opacity = NumericProperty(1)
    star_three_contour_opacity = NumericProperty(1)
    nb_stars = NumericProperty(-1)
    primary_color = ListProperty([0.5, 0.5, 0.5, 1.])
    secondary_color = ListProperty([1., 1., 1., 1.])
    force_border = BooleanProperty(False)

    def __init__(
            self,
            **kwargs):
        self.bind(nb_stars=self.change_nb_stars)
        self.bind(primary_color=self.change_nb_stars)
        self.bind(secondary_color=self.change_nb_stars)
        self.bind(force_border=self.change_nb_stars)
        self.change_nb_stars()
        super().__init__(**kwargs)

    def change_nb_stars(self, base_widget=None, value=None):
        """
        Change the number of stars displayed.
        """

        # self.nb_stars = nb_stars
        if self.nb_stars > 0:
            self.star_one_color = self.secondary_color
            self.star_one_contour_opacity = 1
        else:
            self.star_one_color = (0, 0, 0, 0)
            if not self.force_border:
                self.star_one_contour_opacity = 0
            else:
                self.star_one_contour_opacity = 1
        if self.nb_stars > 1:
            self.star_two_color = self.secondary_color
            self.star_two_contour_opacity = 1
        else:
            self.star_two_color = (0, 0, 0, 0)
            if not self.force_border:
                self.star_two_contour_opacity = 0
            else:
                self.star_two_contour_opacity = 1
        if self.nb_stars > 2:
            self.star_three_color = self.secondary_color
            self.star_three_contour_opacity = 1
        else:
            self.star_three_color = (0, 0, 0, 0)
            if not self.force_border:
                self.star_three_contour_opacity = 0
            else:
                self.star_three_contour_opacity = 1
