from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window

from plyer import notification

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
    do_remember_me = False
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        Window.bind(on_key_down=self.handle_keyboard)
    
    def handle_keyboard(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.password.focus and keycode == 40:
            self.login(self.do_remember_me, self.ids.username.text, self.ids.password.text)
        # print(keycode)
        # # Change focus with tab
        # if self.ids.username.focus and keycode == 43:
        #     self.ids.password.focus = True
    
    def remember_me(self, state):
        if state == "down":
            self.do_remember_me = True
        else:
            self.do_remember_me = False
            
    def login(self, remember_me: bool, username: str, password: str):
        
        login_json = {"remember_me": remember_me, "username": username, "password": password}
        # connect to server and get login response
        try:
            login_status = connect(endpoint="/login", data=login_json)
            if login_status["status"] == True:
                self.manager.push_replacement("home")
            elif login_status["status"] == False:
                # make a popup and request creds again
                notification.notify(title="eNtweniBooking", message="username or password Incorrect", ticker="ticker")
        except Exception as e:
            notification.notify(title="eNtweniBooking", message="Check your connection...", toast=True)
        
        

class PasswordResetScreen(MDScreen):
    # changing screens also can be done in python
    # def goto_home_screen(self):
    #     self.manager.push_replacement("home")
    pass
