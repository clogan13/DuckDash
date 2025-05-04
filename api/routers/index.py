# This file loads all API routers into the FastAPI app.
# Add new routers here to make their endpoints available in the API docs.
from . import orders, order_details, customers, menu, inventory, ingredient, promotions, auth
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to DuckDash API"}

def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(customers.router)
    app.include_router(menu.router)
    app.include_router(inventory.router)
    app.include_router(ingredient.router)
    app.include_router(promotions.router)
    app.include_router(auth.router)
    app.include_router(router)
