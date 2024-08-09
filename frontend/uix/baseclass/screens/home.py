import asyncio

from applibs.connection_manager import EntweniSDKClient

# from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen

# from kivymd.uix.swiper import MDSwiperItem

# Loda kv files TODO: Later optimise for lazy loading
# Builder.load_file("uix/kv/components/organisation_tile.kv")


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.all_organisations = ObjectProperty([])

    def on_pre_enter(self):
        self.client = EntweniSDKClient()
        self.stop_fetching = False
        self.get_organisations()

    def get_organisations(self, *args, **kwargs):
        asyncio.create_task(self.async_get_organisations())

    async def async_get_organisations(self, *args, **kwargs):
        while not self.stop_fetching:
            try:
                response = await self.client.organisations_organisations_get()
                organisations = response.get("organisations")

                return organisations

            except Exception as e:
                print(f"Error fetching organisations: {e}")

            await asyncio.sleep(600)  # Wait for 30 seconds before the next fetch

    def on_leave(self):
        self.stop_fetching = True  # Stop the loop when leaving the screen

    # tab switching logic
    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        # Get corresponding screen name from the manager
        self.current_tab_name = item_text
        self.ids.home_screen_manager.current = item_text
