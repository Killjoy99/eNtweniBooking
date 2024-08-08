from kivy.properties import StringProperty
from kivymd.uix.swiper import MDSwiperItem


class OrganisationTile(MDSwiperItem):
    name = StringProperty("Dummy Organisation")
    image_url = StringProperty()
    description = StringProperty("Dummy Company Description of services Rendered")
    #  Other Infor as we go
