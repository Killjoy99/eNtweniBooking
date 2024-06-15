from kivymd.uix.screen import MDScreen
from kivy_garden.mapview import Coordinate


class MapScreen(MDScreen):
    # changing screens also can be done in python
    # def goto_home_screen(self):
    #     self.manager.push_replacement("home")
    zoom = 10
    zoom_factor = 1
    lat = -20.1457
    lon = 28.5873
    
    driver = Coordinate(lat=lat, lon=lon)
    destination = Coordinate(lon=28.7548, lat=-20.0761)