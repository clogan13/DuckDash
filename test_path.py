import sys
import os

# Print current working directory
print(f"Current working directory: {os.getcwd()}")

# Print Python path
print("\nPython path:")
for path in sys.path:
    print(f"  {path}")

# Try to import from api
try:
    from api.main import app
    print("\nSuccessfully imported from api.main!")
except ImportError as e:
    print(f"\nImport error: {e}") 