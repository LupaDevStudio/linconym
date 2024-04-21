"""
Package to manage the screens of the application
"""

###############
### Imports ###
###############

# Import the custom widgets
from screens.custom_widgets import (
    BottomBar,
    CustomButton,
    ThreeStars,
    SideImageButton,
    RoundedButtonImage,
    ExperienceCounter,
    CircleIconButton,
    RoundButton,
    BoosterLayout,
    ColoredRoundedButton,
    KeyboardLayout,
    ColoredRoundedButtonImage,
    MusicLayout,
    IconCreditLayout,
    GeneralLicensesLayout,
    ImagesCreditLayout,
    LevelCompletedPopup
)

# Import the screens
from screens.home import HomeScreen
from screens.customization import CustomizationScreen
from screens.profile import ProfileScreen
from screens.settings import SettingsScreen
from screens.classic_mode import ClassicModeScreen
from screens.levels import LevelsScreen
from screens.game import GameScreen
from screens.configure_tree import ConfigureTreeScreen
from screens.quests import QuestsScreen
from screens.themes import ThemesScreen
from screens.preview import PreviewScreen
from screens.musics import MusicsScreen
from screens.boosters import BoostersScreen
from screens.badges import BadgesScreen
from screens.achievements import AchievementsScreen
from screens.credits import CreditsScreen
