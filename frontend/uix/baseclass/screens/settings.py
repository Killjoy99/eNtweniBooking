import time

from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

# from kivy_garden.mapview import Coordinate


class SettingsScreen(MDScreen):
    avatar = StringProperty("frontend/data/images/logo.png")


class SettingsAccountScreen(MDScreen):
    def logout(self):
        # Do the logout logic and magic
        time.sleep(0.5)
        self.manager.push_replacement("login")
