import asyncio

from applibs.connection_manager import EntweniSDKClient
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem

# from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from ..components.components import OrganisationTile


class HomeScreen(MDScreen):
    def on_pre_enter(self):
        self.client = EntweniSDKClient()
        self.stop_fetching = False

    def on_enter(self):
        self.get_organisations()

    def get_organisations(self, *args, **kwargs):
        asyncio.create_task(self.async_get_organisations())

    async def async_get_organisations(self, *args, **kwargs):
        while not self.stop_fetching:
            try:
                response = await self.client.organisations_organisations_get()
                organisations = response.get("organisations", [])

                if organisations:
                    # self.ids.organisation_list.clear_widgets()  # Clear existing widgets
                    for organisation in organisations:
                        self.ids.organisation_list.add_widget(OrganisationTile())
                else:
                    self.add_widget(
                        MDLabel(
                            text="[size=20sp][color=#ff0000]No Registered Service Providers Yet[/color][/size]",
                            markup=True,
                            pos_hint={"center_x": 0.5, "center_y": 0.5},
                        )
                    )

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
        self.ids.home_screen_manager.current = item_text
