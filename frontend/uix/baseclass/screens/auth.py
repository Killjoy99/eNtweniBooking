from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty

from applibs.connections import connect


class WelcomeScreen(MDScreen):
    logo = ObjectProperty("data/images/logo.png")
    status = StringProperty()
    data = StringProperty()
    try:
        data = connect()
        if not data:
            status = "offline"
        else:
            status = "online"
    except Exception as e:
        pass

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
