"""
Main FastAPI application with authentication and protected routes.
"""
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import orders, order_details, customers, menu, inventory, ingredients
from .controllers import auth
from .dependencies.auth import get_current_user
from .models import model_loader
from .dependencies.config import conf


app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(orders.router, dependencies=[Depends(get_current_user)])
app.include_router(order_details.router, dependencies=[Depends(get_current_user)])
app.include_router(customers.router, dependencies=[Depends(get_current_user)])
app.include_router(menu.router, dependencies=[Depends(get_current_user)])
app.include_router(inventory.router, dependencies=[Depends(get_current_user)])
app.include_router(ingredients.router, dependencies=[Depends(get_current_user)])

@app.get("/")
def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to DuckDash API"}

model_loader.index()