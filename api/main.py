"""
Main FastAPI application with authentication and protected routes.
"""
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers.index import load_routes
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

# Use load_routes to register all routers, including promotions
load_routes(app)

@app.get("/")
def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to DuckDash API"}

model_loader.index()