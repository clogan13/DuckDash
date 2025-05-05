# This file loads all API routers into the FastAPI app.
# Add new routers here to make their endpoints available in the API docs.
from fastapi import FastAPI

# Import all routers
from api.routers import orders, order_details, customers, menu, inventory, ingredient, promotions, auth, feedback

def load_routes(app: FastAPI):
    """
    Load all routes into the FastAPI application
    """
    app.include_router(orders.router, prefix="/orders", tags=["orders"])
    app.include_router(order_details.router, prefix="/order-details", tags=["order-details"])
    app.include_router(customers.router, prefix="/customers", tags=["customers"])
    app.include_router(menu.router, prefix="/menu", tags=["menu"])
    app.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
    app.include_router(ingredient.router, prefix="/ingredient", tags=["ingredient"])
    app.include_router(promotions.router, prefix="/promotions", tags=["promotions"])
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
