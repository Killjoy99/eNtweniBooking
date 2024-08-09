from auth.models import User
from booking.models import Booking
from organisation.models import Organisation
from product.models import Product
from sqladmin import ModelView


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
