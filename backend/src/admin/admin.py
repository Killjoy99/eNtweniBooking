from kivy.uix.modalview import ModalView
from sqladmin import ModelView
from src.auth.models import User
from src.organisation.models import Organisation
from src.product.models import Product


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.username]


class OrganisationAdmin(ModelView, model=Organisation):
    column_list = [Organisation.id, Organisation.name, Organisation.description]
    
    
class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name, Product.description]