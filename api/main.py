"""
Main FastAPI application with authentication and protected routes.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.index import load_routes
from api.models import model_loader
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Serve the frontend files
@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.get("/login")
def login():
    return FileResponse("frontend/login.html")

@app.get("/signup")
def signup():
    return FileResponse("frontend/signup.html")

@app.get("/profile")
def profile():
    return FileResponse("frontend/profile.html")

@app.get("/checkout")
def checkout():
    return FileResponse("frontend/checkout.html")

@app.get("/contact")
def contact():
    return FileResponse("frontend/contact.html")

@app.get("/order")
def order():
    return FileResponse("frontend/order.html")

# model_loader.index()  # Disabled to prevent data loss on server restart