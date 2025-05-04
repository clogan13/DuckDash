# This file loads all API routers into the FastAPI app.
# Add new routers here to make their endpoints available in the API docs.
from . import orders, order_details, customers, menu


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(customers.router)
    app.include_router(menu.router)
