import asyncio

from applibs.connection_manager import EntweniSDKClient
from kivy.properties import BooleanProperty
from kivymd.uix.screen import MDScreen


class HomeScreen(MDScreen):
    no_organisations = BooleanProperty()

    def on_pre_enter(self):
        self.client = EntweniSDKClient()

    def on_enter(self):
        self.get_organisations()

    def get_organisations(self, *args, **kwargs):
        asyncio.create_task(self.async_get_organisations())

    async def async_get_organisations(self, *args, **kwargs):
        organisations = await self.client.organisations_organisations_get()

        if not organisations:
            self.no_organisations = True

        # self.root.
