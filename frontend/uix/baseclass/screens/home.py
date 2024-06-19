from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel

from applibs.connections import connect


class HomeScreen(MDScreen):
    
    def on_pre_enter(self):
        self.organisations = self.get_organisations()
        self.products = self.get_products()
        self.bookings = self.get_bookings()
        
    def on_enter(self):
        self.add_organisations()

    
    ############################## ORGANISATIONS ##############################
    def add_organisations(self):
        for organisation in self.organisations:
            self.ids.organisation_list.add_widget(MDLabel(text=organisation["name"]))
    
    def get_organisations(self):
        try:
            organisations = connect(endpoint="/api/v1/organisations")
            if not organisations:
                return None
            return organisations
        except Exception as e:
            pass


    ############################## PRODUCTS ##############################
    def get_products(self):
        try:
            products = connect(endpoint="/api/v1/products")
            if not products:
                return None
            return products
        except Exception as e:
            pass

    ############################## BOOKINGS ##############################
    def get_bookings(self):
        try:
            bookings = connect(endpoint="/api/v1/bookings")
            if not bookings:
                return None
            return bookings
        except Exception as e:
            pass