from . import Customer, Feedback, Orders, Promotion, Payment, Menu, Inventory, order_details

from ..dependencies.database import engine


def index():

    Customer.Base.metadata.create_all(engine)
    Feedback.Base.metadata.create_all(engine)
    Inventory.Base.metadata.create_all(engine)
    Menu.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    Orders.Base.metadata.create_all(engine)
    Payment.Base.metadata.create_all(engine)
    Promotion.Base.metadata.create_all(engine)

