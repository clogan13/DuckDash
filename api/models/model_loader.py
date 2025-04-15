from . import Customer, Feedback, Orders, Promotion, Payment, Menu, Inventory

from ..dependencies.database import engine


def index():

    Customer.Base.metadata.create_all(engine)
    Feedback.Base.metadata.create_all(engine)
    Inventory.Base.metadata.create_all(engine)
    Menu.Base.metadata.create_all(engine)
    Orders.Base.metadata.create_all(engine)
    Payment.Base.metadata.create_all(engine)
    Promotion.Base.metadata.create_all(engine)

