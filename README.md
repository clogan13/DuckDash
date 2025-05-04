# DuckDash

Final Project for ITSC-3155-051

DuckDash is a modern restaurant order management API built with FastAPI, SQLAlchemy, and MySQL. It supports user authentication, menu management, order processing, inventory, and more.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/clogan13/DuckDash.git
cd DuckDash
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Set Up the Database
- Make sure you have MySQL running.
- Edit `api/dependencies/config.py` with your DB credentials if needed.
- Run the schema to create all tables:
  - In MySQL Workbench or CLI:
    ```sql
    SOURCE schema.sql;
    ```
  - Or, from Python:
    ```bash
    python -c "from api.models.model_loader import index; index()"
    ```

### 4. Run the Server
```bash
uvicorn api.main:app --reload
```

### 5. Test the API
- Open your browser to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive Swagger UI.
- You can register, login, and try all endpoints directly from the docs.

---

## 📦 Project Structure
```
DuckDash/
├── api/                # Main application code
│   ├── controllers/    # Business logic
│   ├── dependencies/   # DB config, auth, etc.
│   ├── models/         # SQLAlchemy models
│   ├── routers/        # API endpoints
│   ├── schemas/        # Pydantic schemas
│   └── scripts/        # Utility scripts (e.g., data seeding)
├── docs/               # Feature documentation
│   └── features/       # Detailed feature docs
├── tests/              # Test cases
├── requirements.txt    # Python dependencies
├── schema.sql          # MySQL schema (share with your group!)
└── README.md           # This file
```

---

## 🛠️ Features
- **User Authentication**
  - Registration & login with JWT
  - Protected endpoints for staff operations
- **Menu Management**
  - Public menu browsing with filters (category, dietary, price)
  - Protected endpoints for menu modifications
  - Sample menu data seeding
- **Order Processing**
  - Customer order creation
  - Order tracking and management
- **Additional Features**
  - Inventory management
  - Customer feedback
  - Analytics and reporting

---

## 📖 Documentation
Detailed documentation for each feature is available in the `docs/features/` directory:
- [Menu Browsing](docs/features/menu_browsing.md) - Complete guide to menu endpoints and filtering
- More feature documentation coming soon!

---

## 👥 For Group Members
- Use `requirements.txt` to install dependencies
- Use `schema.sql` to set up your database
- Check the documentation in `docs/features/` for implementation details
- All code is commented and ready for collaboration

---

## 📚 Resources
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Project Repository](https://github.com/clogan13/DuckDash)

---

Happy coding! 🦆

## Documentation

- [API Documentation](docs/api.md)
- [Database Schema](docs/database.md)
- [Authentication System](docs/authentication.md)
- [Order System](docs/orders.md)
- [Promotion System](docs/promotion_system.md)