import asyncio

from applibs.connection_manager import EntweniSDKClient
from kivymd.uix.screen import MDScreen


class HomeScreen(MDScreen):
    def on_pre_enter(self):
        self.client = EntweniSDKClient()

    def on_enter(self):
        self.health_check()

    def health_check(self):
        asyncio.create_task(self.client.healthcheck_healthcheck_get())
