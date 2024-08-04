import asyncio

from applibs.connection_manager import EntweniSDKClient
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.screen import MDScreen


class WelcomeScreen(MDScreen):
    logo = ObjectProperty("data/images/logo.png")
    status = StringProperty()
    data = StringProperty()

    def on_pre_enter(self):
        self.client = EntweniSDKClient()

    def on_enter(self):
        self.health_check()

    def health_check(self):
        asyncio.create_task(self.async_health_check())

    async def async_health_check(self):
        status = await self.client.healthcheck_healthcheck_get()

        if status.get("detail") == "STATUS_OK":
            self.status = "online"
        else:
            self.status = "offline"


class RegisterScreen(MDScreen):
    # changing screens also can be done in python
    # def goto_home_screen(self):
    #     self.manager.push_replacement("home")
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)

        Window.bind(on_key_down=self.handle_keyboard)

    def handle_keyboard(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.password_confirm.focus and keycode == 40:
            self.register(
                username=self.ids.username.text,
                email=self.ids.email.text,
                first_name=self.ids.first_name.text,
                last_name=self.ids.last_name.text,
                password=self.ids.password_confirm.text,
            )

    def on_pre_enter(self):
        self.client = EntweniSDKClient()

    def register(self, **kwargs):
        asyncio.create_task(self.async_register())

    async def async_register(self, *args, **kwargs):
        register_json = {
            "username": kwargs.get("username"),
            "email": kwargs.get("email"),
            "first_name": kwargs.get("first_name"),
            "last_name": kwargs.get("last_name"),
            "password": kwargs.get("password"),
        }
        register_response = await self.client.register_register__post(
            data=register_json
        )
        # check the type of register_response and populate errors accordingly
        if register_response.get("status_code") == 302:
            self.root.push("home")


class LoginScreen(MDScreen):
    """A Screen with a list of all supported countries that can register on the app"""

    do_remember_me = False

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        Window.bind(on_key_down=self.handle_keyboard)

    def handle_keyboard(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.password.focus and keycode == 40:
            self.login(
                self.do_remember_me,
                self.ids.login_identifier.text,
                self.ids.password.text,
            )

    def on_pre_enter(self):
        self.client = EntweniSDKClient()

    def remember_me(self, state):
        if state == "down":
            self.do_remember_me = True
        else:
            self.do_remember_me = False

    def login(self, remember_me: bool, login_identifier: str, password: str):
        asyncio.create_task(
            self.async_login(login_identifier=login_identifier, password=password)
        )

    async def async_login(self, *args, **kwargs):
        login_json = {
            "login_identifier": kwargs.get("login_identifier"),
            "password": kwargs.get("password"),
        }
        login_response = await self.client.login_login__post(data=login_json)
        # try and see if we received the cookies
        # TODO: Retrieve and Store the cookies for automatic login {Store in a local database}
        # check the response we get and handle accordingly
        if login_response.get("detail") == "LOGIN_SUCCESS":
            self.manager.push_replacement("home")

        print(login_response.get("detail"))


class PasswordResetScreen(MDScreen):
    # changing screens also can be done in python
    # def goto_home_screen(self):
    #     self.manager.push_replacement("home")
    pass
