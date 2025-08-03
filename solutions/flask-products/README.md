# 🐍 Flask Product Management API with MCP Integration

A comprehensive Flask-based REST API for product management with full CRUD operations, data validation, error handling, and MCP (Model Context Protocol) integration. This project serves as a practical example for the MCP workshop, demonstrating how to build MCP-compatible APIs.

## 📋 Features

### Core Functionality
- ✅ **Product Management**: Complete CRUD operations for products
- ✅ **REST API**: RESTful endpoints with proper HTTP status codes  
- ✅ **Data Validation**: Input validation using Marshmallow schemas
- ✅ **Error Handling**: Comprehensive error handling with standardized responses
- ✅ **Database Integration**: SQLAlchemy ORM with SQLite (configurable)
- ✅ **Search & Filtering**: Search products and filter by category
- ✅ **Pagination**: Paginated responses for list endpoints
- ✅ **MCP Integration**: Expose API operations as MCP tools

### Product Schema
```json
{
  "id": "integer (auto-increment)",
  "name": "string (required, max 100 chars)",
  "description": "text (optional)",
  "price": "decimal (required, positive)",
  "category": "string (required)",
  "stock_quantity": "integer (default 0)",
  "sku": "string (unique, required)",
  "created_at": "datetime (auto)",
  "updated_at": "datetime (auto)"
}
```

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/api` | API information |
| `GET` | `/api/products` | List all products (with pagination) |
| `GET` | `/api/products/{id}` | Get single product |
| `POST` | `/api/products` | Create new product |
| `PUT` | `/api/products/{id}` | Update existing product |
| `DELETE` | `/api/products/{id}` | Delete product |
| `GET` | `/api/products/search?q=term` | Search products |
| `GET` | `/api/products/category/{category}` | Filter by category |
| `GET` | `/api/products/categories` | Get all categories |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### 1. Setup Environment

```bash
# Clone the repository (if not already in workshop)
cd solutions/flask-products

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Flask API

```bash
# Run the development server
python run.py

# Or run directly
python app.py
```

The API will be available at `http://localhost:5000`

### 3. Test the API

```bash
# Health check
curl http://localhost:5000/health

# Get API info
curl http://localhost:5000/api

# List products
curl http://localhost:5000/api/products

# Create a product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Laptop",
    "description": "High-performance gaming laptop",
    "price": 1299.99,
    "category": "Electronics", 
    "stock_quantity": 5,
    "sku": "GAME-LAP-001"
  }'
```

### 4. Run MCP Server

```bash
# Run the MCP server
python mcp/server.py
```

### 5. Test MCP Integration

```bash
# Install MCP inspector (if not already installed)
npm install -g @modelcontextprotocol/inspector

# Test MCP server tools
npx @modelcontextprotocol/inspector --cli mcp run mcp/server.py --method tools/list

# Test a specific tool
npx @modelcontextprotocol/inspector --cli mcp run mcp/server.py --method tools/call --tool-name list_products
```

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies (included in requirements.txt)
pip install pytest pytest-flask

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

### Test Coverage
The test suite includes:
- ✅ Model tests (Product creation, validation, serialization)
- ✅ API endpoint tests (CRUD operations, error handling)
- ✅ Integration tests (database operations, pagination)
- ✅ Validation tests (input validation, error responses)

## 📁 Project Structure

```
flask-products/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── run.py                # Application entry point
├── requirements.txt      # Dependencies
├── models/
│   ├── __init__.py
│   └── product.py        # Product model
├── routes/
│   ├── __init__.py
│   └── products.py       # Product routes
├── utils/
│   ├── __init__.py
│   ├── validators.py     # Input validation schemas
│   └── responses.py      # Response helpers
├── tests/
│   ├── __init__.py
│   ├── test_products.py  # Model tests
│   └── test_api.py       # API tests
├── mcp/
│   ├── __init__.py
│   └── server.py         # MCP server integration
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

```bash
# Flask configuration
FLASK_ENV=development          # development, testing, production
SECRET_KEY=your-secret-key     # Flask secret key
DEBUG=True                     # Debug mode

# Database configuration  
DATABASE_URL=sqlite:///products.db  # Database connection string
SQLALCHEMY_ECHO=False              # Log SQL queries

# API configuration
PRODUCTS_PER_PAGE=20          # Default pagination size
CORS_ORIGINS=*                # CORS allowed origins

# Server configuration
HOST=0.0.0.0                  # Server host
PORT=5000                     # Server port
```

### Configuration Files
- `config.py`: Main configuration classes
- `.env`: Environment variables (create this file)

## 🔌 MCP Integration

### MCP Tools Available

The MCP server exposes the following tools:

1. **`list_products`** - List products with pagination and filtering
2. **`get_product`** - Get a single product by ID
3. **`create_product`** - Create a new product
4. **`update_product`** - Update an existing product
5. **`delete_product`** - Delete a product
6. **`search_products`** - Search products by name, description, or SKU
7. **`get_products_by_category`** - Get products by category
8. **`get_categories`** - Get all product categories

### Usage Examples

```bash
# List all MCP tools
npx @modelcontextprotocol/inspector --cli mcp run mcp/server.py --method tools/list

# Create a product via MCP
npx @modelcontextprotocol/inspector --cli mcp run mcp/server.py \
  --method tools/call \
  --tool-name create_product \
  --tool-arg name="MCP Product" \
  --tool-arg price=99.99 \
  --tool-arg category="Test" \
  --tool-arg sku="MCP-001"

# Search products via MCP
npx @modelcontextprotocol/inspector --cli mcp run mcp/server.py \
  --method tools/call \
  --tool-name search_products \
  --tool-arg query="laptop"
```

## 📊 API Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": {
    // Response data here
  }
}
```

### Error Response
```json
{
  "status": "error", 
  "message": "Error description",
  "errors": {
    // Field-specific errors (for validation errors)
  }
}
```

### Paginated Response
```json
{
  "status": "success",
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 100,
      "pages": 5,
      "has_prev": false,
      "has_next": true,
      "prev_url": null,
      "next_url": "/api/products?page=2"
    }
  }
}
```

## 🎯 Workshop Exercises

### Exercise 1: Setup and Basic API
- [ ] Set up the Flask application
- [ ] Create the Product model
- [ ] Implement basic CRUD endpoints
- [ ] Test with sample data

### Exercise 2: Validation and Error Handling
- [ ] Add Marshmallow validation schemas
- [ ] Implement comprehensive error handling
- [ ] Test validation edge cases
- [ ] Add proper HTTP status codes

### Exercise 3: Search and Filtering
- [ ] Implement search functionality
- [ ] Add category filtering
- [ ] Add pagination support
- [ ] Test search edge cases

### Exercise 4: MCP Integration
- [ ] Create MCP server with product tools
- [ ] Test MCP tools with inspector
- [ ] Integrate with MCP client
- [ ] Document MCP integration patterns

### Exercise 5: Testing and Documentation
- [ ] Write comprehensive unit tests
- [ ] Add integration tests
- [ ] Create API documentation
- [ ] Test error scenarios

## 🔍 Development Tips

### Database Operations
```bash
# Create database tables
python -c "from app import create_app; from models.product import db; app = create_app(); app.app_context().push(); db.create_all()"

# Reset database
python -c "from app import create_app; from models.product import db; app = create_app(); app.app_context().push(); db.drop_all(); db.create_all()"
```

### Sample Data
```python
# Add sample products (run in Python shell)
from app import create_app
from models.product import db, Product

app = create_app()
with app.app_context():
    product = Product(
        name="Sample Product",
        description="This is a sample product",
        price=29.99,
        category="Sample",
        stock_quantity=10,
        sku="SAMPLE-001"
    )
    db.session.add(product)
    db.session.commit()
```

## 🐛 Troubleshooting

### Common Issues

1. **Database not found**
   ```bash
   # Solution: Initialize database
   python -c "from app import create_app; from models.product import db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

2. **MCP server not starting**
   ```bash
   # Solution: Install MCP dependencies
   pip install mcp
   ```

3. **Import errors**
   ```bash
   # Solution: Ensure you're in the virtual environment
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

4. **Port already in use**
   ```bash
   # Solution: Use a different port
   export PORT=5001
   python run.py
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is part of the MCP Workshop and is intended for educational purposes.

## 🔗 Related Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Marshmallow Documentation](https://marshmallow.readthedocs.io/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Workshop](../README.md)

---

**Happy coding! 🎉**