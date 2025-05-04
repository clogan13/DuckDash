# config.py
# This file contains configuration variables for database and app connection.
class conf:
    # Database configuration
    db_host = "localhost"         # Database host
    db_name = "Duckdash"          # Database name
    db_port = 3306                # Database port (default MySQL)
    db_user = "root"              # Database username
    db_password = "icis"          # Database password
    
    # App configuration
    app_host = "localhost"        # App host
    app_port = 8000               # App port
    
    # JWT configuration
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Change this in production!
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30