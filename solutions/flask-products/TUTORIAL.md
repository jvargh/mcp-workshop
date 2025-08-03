# Flask Product Management API Workshop Tutorial

## Overview
This tutorial walks you through building a complete Flask REST API with MCP integration. You'll learn how to create a product management system that can be exposed through the Model Context Protocol.

## Learning Objectives
By the end of this tutorial, you will:
- ✅ Build a Flask REST API with CRUD operations
- ✅ Implement data validation and error handling
- ✅ Create an MCP server that exposes API functionality
- ✅ Write comprehensive tests for your API
- ✅ Understand Flask best practices and project structure

## Prerequisites
- Python 3.8+
- Basic understanding of REST APIs
- Familiarity with Flask (helpful but not required)
- Understanding of MCP concepts from previous workshops

## Workshop Structure

### Part 1: Flask API Fundamentals (30 minutes)
**Objective**: Set up a basic Flask application with product models

1. **Environment Setup**
   ```bash
   cd solutions/flask-products
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

2. **Explore the Project Structure**
   - `app.py` - Main Flask application
   - `models/product.py` - Product data model
   - `config.py` - Configuration management
   - `routes/products.py` - API endpoints

3. **Run the Application**
   ```bash
   python run.py
   ```

4. **Test Basic Endpoints**
   ```bash
   # Health check
   curl http://localhost:5000/health
   
   # API info
   curl http://localhost:5000/api
   ```

### Part 2: CRUD Operations (45 minutes)
**Objective**: Implement and test all product management operations

1. **Create a Product**
   ```bash
   curl -X POST http://localhost:5000/api/products \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Workshop Laptop",
       "description": "A laptop for the MCP workshop",
       "price": 899.99,
       "category": "Electronics",
       "stock_quantity": 10,
       "sku": "WS-LAP-001"
     }'
   ```

2. **List Products**
   ```bash
   curl http://localhost:5000/api/products
   ```

3. **Get Single Product**
   ```bash
   curl http://localhost:5000/api/products/1
   ```

4. **Update Product**
   ```bash
   curl -X PUT http://localhost:5000/api/products/1 \
     -H "Content-Type: application/json" \
     -d '{"price": 799.99, "stock_quantity": 15}'
   ```

5. **Search Products**
   ```bash
   curl "http://localhost:5000/api/products/search?q=laptop"
   ```

6. **Filter by Category**
   ```bash
   curl http://localhost:5000/api/products/category/Electronics
   ```

### Part 3: Data Validation & Error Handling (30 minutes)
**Objective**: Understand input validation and error responses

1. **Test Validation Errors**
   ```bash
   # Try creating invalid product
   curl -X POST http://localhost:5000/api/products \
     -H "Content-Type: application/json" \
     -d '{"name": "", "price": -100}'
   ```

2. **Explore Validation Rules**
   - Look at `utils/validators.py`
   - Understand Marshmallow schemas
   - Test different validation scenarios

3. **Error Response Format**
   - Standardized error responses
   - Proper HTTP status codes
   - Field-specific validation errors

### Part 4: MCP Integration (45 minutes)
**Objective**: Create and test MCP server integration

1. **Run the MCP Server**
   ```bash
   python mcp/server.py
   ```

2. **List Available MCP Tools**
   ```bash
   npx @modelcontextprotocol/inspector --cli mcp run mcp/server.py --method tools/list
   ```

3. **Test MCP Tools**
   ```bash
   # Create product via MCP
   npx @modelcontextprotocol/inspector --cli mcp run mcp/server.py \
     --method tools/call \
     --tool-name create_product \
     --tool-arg name="MCP Product" \
     --tool-arg price=99.99 \
     --tool-arg category="Test" \
     --tool-arg sku="MCP-001"
   
   # List products via MCP
   npx @modelcontextprotocol/inspector --cli mcp run mcp/server.py \
     --method tools/call \
     --tool-name list_products
   ```

4. **Understand MCP Integration**
   - How Flask API operations become MCP tools
   - Tool parameter validation
   - Response formatting for MCP

### Part 5: Testing (30 minutes)
**Objective**: Run and understand the test suite

1. **Run All Tests**
   ```bash
   pytest tests/ -v
   ```

2. **Run Specific Test Categories**
   ```bash
   # Model tests only
   pytest tests/test_products.py -v
   
   # API tests only  
   pytest tests/test_api.py -v
   ```

3. **Understand Test Structure**
   - Test fixtures and setup
   - Model unit tests
   - API integration tests
   - Test database usage

4. **Test Coverage**
   ```bash
   pytest --cov=. --cov-report=html
   # Open htmlcov/index.html to see coverage report
   ```

## Exercises

### Exercise 1: Add New Product Field
Add a "weight" field to the Product model:
1. Update `models/product.py`
2. Update validation schemas in `utils/validators.py`
3. Update tests
4. Test the changes

### Exercise 2: Implement Bulk Operations
Add endpoints for bulk product operations:
1. `POST /api/products/bulk` - Create multiple products
2. `PUT /api/products/bulk` - Update multiple products
3. Add corresponding MCP tools

### Exercise 3: Add Authentication
Implement JWT-based authentication:
1. Add user model and authentication
2. Protect product endpoints
3. Update MCP integration for auth

### Exercise 4: Enhanced Search
Improve search functionality:
1. Add full-text search
2. Add price range filtering
3. Add sorting options
4. Update MCP tools accordingly

## Best Practices Demonstrated

### Flask Application Structure
- **Blueprints**: Organized route registration
- **Application Factory**: Configurable app creation
- **Configuration Management**: Environment-based config
- **Database Integration**: SQLAlchemy ORM usage

### API Design
- **RESTful Endpoints**: Standard HTTP methods and URLs
- **Consistent Responses**: Standardized JSON format
- **Error Handling**: Proper HTTP status codes
- **Input Validation**: Comprehensive data validation

### MCP Integration
- **Tool Mapping**: Flask operations as MCP tools
- **Parameter Validation**: Input validation for MCP tools
- **Response Formatting**: Consistent MCP responses
- **Documentation**: Well-documented tool schemas

### Testing Strategy
- **Unit Tests**: Model and utility testing
- **Integration Tests**: Full API endpoint testing
- **Test Fixtures**: Reusable test data
- **Test Coverage**: Comprehensive test coverage

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Solution: Use different port
   export PORT=5001
   python run.py
   ```

2. **Database Issues**
   ```bash
   # Solution: Reset database
   rm instance/products.db
   python run.py
   ```

3. **Import Errors**
   ```bash
   # Solution: Ensure virtual environment is active
   source venv/bin/activate
   ```

4. **MCP Inspector Not Found**
   ```bash
   # Solution: Install globally
   npm install -g @modelcontextprotocol/inspector
   ```

## Next Steps

After completing this workshop:
1. **Extend the API**: Add more features like categories, suppliers, orders
2. **Deploy the Application**: Use Docker, Heroku, or other platforms
3. **Build a Frontend**: Create a React/Vue.js frontend
4. **Integrate with Other MCPs**: Connect with other MCP servers
5. **Production Hardening**: Add logging, monitoring, security features

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Marshmallow Validation](https://marshmallow.readthedocs.io/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [REST API Best Practices](https://restfulapi.net/)

---

**Happy coding! 🎉 You've built a complete Flask API with MCP integration!**