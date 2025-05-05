"""
Main FastAPI application with authentication and protected routes.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.index import load_routes
from api.models import model_loader
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load all routes
load_routes(app)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to DuckDash API"}

# model_loader.index()  # Disabled to prevent data loss on server restart