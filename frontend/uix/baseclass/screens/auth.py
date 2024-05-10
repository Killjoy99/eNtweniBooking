from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

class WelcomeScreen(MDScreen):
    logo = ObjectProperty("data/images/logo.png")

class RegisterScreen(MDScreen):
    # changing screens also can be done in python
    # def goto_home_screen(self):
    #     self.manager.push_replacement("home")
    pass


class LoginScreen(MDScreen):
    """ A Screen with a list of all supported countries that can register on the app"""
    pass

class PasswordResetScreen(MDScreen):
    # changing screens also can be done in python
    # def goto_home_screen(self):
    #     self.manager.push_replacement("home")
    pass
