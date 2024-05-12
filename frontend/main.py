import asyncio

from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.core.window import Window

from uix.root import Root


# Resize the window to mimic the android screen size
Window.size = (400, 840)

class EntweniBooking(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.light_theme_color = "#008080"
        
        # set theme
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        # self.store = JsonStore("config.json")
        self.title = "EntweniBooking"
        self.icon = "data/images/logo.jpg"
        # self.registered = self.check_registered()

        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"
        
    def build(self):
        self.root = Root()
        self.root.push("welcome")


if __name__ == "__main__":
    app = EntweniBooking()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(app.async_run(async_lib="asyncio"))