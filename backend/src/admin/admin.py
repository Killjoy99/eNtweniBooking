from sqladmin import ModelView

from src.auth.models import User
from src.booking.models import Booking
from src.organisation.models import Organisation
from src.product.models import Product


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.username, User.last_login]


class OrganisationAdmin(ModelView, model=Organisation):
    column_list = [
        Organisation.id,
        Organisation.name,
        Organisation.description,
        Organisation.active,
        Organisation.is_deleted,
    ]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name, Product.description]


class BookingAdmin(ModelView, model=Booking):
    column_list = [
        Booking.id,
        Booking.description,
        Booking.created_at,
        Booking.updated_at,
        Booking.is_deleted,
    ]
