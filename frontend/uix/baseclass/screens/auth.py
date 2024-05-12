from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty

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
                print("Incorrect credentials")
        except Exception as e:
            print("You are offline")
        
        

class PasswordResetScreen(MDScreen):
    # changing screens also can be done in python
    # def goto_home_screen(self):
    #     self.manager.push_replacement("home")
    pass
