"""
Module for the opening screen.
"""

###############
### Imports ###
###############

import os
from threading import Thread
from tools.kivy_tools import ImprovedScreen
from tools.path import (
    PATH_IMAGES
)
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label


class OpeningScreen(ImprovedScreen):
    """
    Screen of Opening.
    """

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "opening.jpg",
            **kw)
        self.opacity_state = -1
        self.opacity_rate = 0.03
        self.label = Label(text="", pos_hint={
            "bottom": 1, "left": 1})
        self.add_widget(self.label)

    def update(self, *args):
        self.label.opacity += self.opacity_state * self.opacity_rate
        if self.label.opacity < 0 or self.label.opacity > 1:
            self.opacity_state = -self.opacity_state

    def on_enter(self, *args):
        # Schedule the update for the text opacity effect
        Clock.schedule_interval(self.update, 1 / 60)

        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        # Unschedule the clock update
        Clock.unschedule(self.update, 1 / 60)

        return super().on_leave(*args)

    def launch_thread(self, *_):
        thread = Thread(target=self.load_kv_files)
        thread.start()

    def load_kv_files(self, *_):
        from screens import (
            HomeScreen,
            SettingsScreen,
            ProfileScreen,
            ThemesScreen,
            ClassicModeScreen,
            BoostersScreen,
            LevelsScreen,
            CustomizationScreen,
            GameScreen,
            QuestsScreen,
            CreditsScreen,
            PreviewScreen,
            MusicsScreen,
            ConfigureTreeScreen,
            AchievementsScreen,
            BadgesScreen,
            LegendModeScreen
        )

        screen_files = [file for file in os.listdir(
            "screens") if file.endswith(".kv")]
        for file in screen_files:
            Builder.load_file(f"screens/{file}", encoding="utf-8")
        widget_files = [file for file in os.listdir(
            "screens/custom_widgets") if file.endswith(".kv")]
        for file in widget_files:
            Builder.load_file(
                f"screens/custom_widgets/{file}", encoding="utf-8")
        for package in ["button", "layout", "popup"]:
            widget_files = [file for file in os.listdir(
                f"screens/custom_widgets/{package}") if file.endswith(".kv")]
            for file in widget_files:
                Builder.load_file(
                    f"screens/custom_widgets/{package}/{file}", encoding="utf-8")

        self.HomeScreen = HomeScreen
        self.SettingsScreen = SettingsScreen
        self.ProfileScreen = ProfileScreen
        self.ThemesScreen = ThemesScreen
        self.ClassicModeScreen = ClassicModeScreen
        self.BoostersScreen = BoostersScreen
        self.LevelsScreen = LevelsScreen
        self.CustomizationScreen = CustomizationScreen
        self.GameScreen = GameScreen
        self.QuestsScreen = QuestsScreen
        self.CreditsScreen = CreditsScreen
        self.PreviewScreen = PreviewScreen
        self.MusicsScreen = MusicsScreen
        self.ConfigureTreeScreen = ConfigureTreeScreen
        self.AchievementsScreen = AchievementsScreen
        self.BadgesScreen = BadgesScreen
        self.LegendModeScreen = LegendModeScreen

        Clock.schedule_once(self.load_other_screens)

    def switch_to_menu(self, *args):
        self.manager.current = "home"

    def load_other_screens(self, *args):

        ### Load the kv files of the screens ###

        home_screen = self.HomeScreen(name="home")
        self.manager.add_widget(home_screen)

        settings_screen = self.SettingsScreen(name="settings")
        self.manager.add_widget(settings_screen)

        profile_screen = self.ProfileScreen(name="profile")
        self.manager.add_widget(profile_screen)

        themes_screen = self.ThemesScreen(name="themes")
        self.manager.add_widget(themes_screen)

        classic_mode_screen = self.ClassicModeScreen(name="classic_mode")
        self.manager.add_widget(classic_mode_screen)

        legend_mode_screen = self.LegendModeScreen(name="legend_mode")
        self.manager.add_widget(legend_mode_screen)

        boosters_screen = self.BoostersScreen(name="boosters")
        self.manager.add_widget(boosters_screen)

        levels_screen = self.LevelsScreen(name="levels")
        self.manager.add_widget(levels_screen)

        game_screen = self.GameScreen(name="game")
        self.manager.add_widget(game_screen)

        quests_screen = self.QuestsScreen(name="quests")
        self.manager.add_widget(quests_screen)

        customization_screen = self.CustomizationScreen(name="customization")
        self.manager.add_widget(customization_screen)
        
        credits_screen = self.CreditsScreen(name="credits")
        self.manager.add_widget(credits_screen)

        preview_screen = self.PreviewScreen(name="preview")
        self.manager.add_widget(preview_screen)

        musics_screen = self.MusicsScreen(name="musics")
        self.manager.add_widget(musics_screen)

        configure_tree_screen = self.ConfigureTreeScreen(name="configure_tree")
        self.manager.add_widget(configure_tree_screen)

        achievements_screen = self.AchievementsScreen(name="achievements")
        self.manager.add_widget(achievements_screen)

        badges_screen = self.BadgesScreen(name="badges")
        self.manager.add_widget(badges_screen)

        Clock.schedule_once(self.switch_to_menu)
