import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from routers.index import load_routes
    from models import model_loader
    print("All imports successful!")
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current sys.path: {sys.path}") 