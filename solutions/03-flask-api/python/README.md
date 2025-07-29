# Flask Products API

A Python Flask REST API for managing products with full CRUD (Create, Read, Update, Delete) operations. This API uses in-memory storage and includes basic validation.

## Features

- **CRUD Operations**: Create, read, update, and delete products
- **In-Memory Storage**: Products are stored in memory (data is lost when server restarts)
- **Input Validation**: Basic validation for product data
- **Filtering**: Filter products by category, price range
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Sample Data**: Pre-loaded with sample products for testing

## Product Schema

Each product has the following fields:

```json
{
  "id": "unique-uuid",
  "name": "string (required, max 100 chars)",
  "description": "string (required, max 500 chars)",
  "price": "number (required, non-negative)",
  "category": "string (optional)",
  "created_at": "ISO datetime string",
  "updated_at": "ISO datetime string"
}
```

## Setup and Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
source ./venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000` with sample data pre-loaded.

## API Endpoints

### Health Check
- **GET** `/health` - Check if the API is running

### Products

#### List Products
- **GET** `/products` - Get all products
- **Query Parameters:**
  - `category` - Filter by category (case-insensitive)
  - `min_price` - Filter by minimum price
  - `max_price` - Filter by maximum price

#### Create Product
- **POST** `/products` - Create a new product
- **Body:** JSON with `name`, `description`, `price` (required), and `category` (optional)

#### Get Product
- **GET** `/products/{id}` - Get a specific product by ID

#### Update Product
- **PUT** `/products/{id}` - Update an existing product
- **Body:** JSON with any combination of `name`, `description`, `price`, `category`

#### Delete Product
- **DELETE** `/products/{id}` - Delete a product

## Usage Examples

### 1. Check API Health

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### 2. List All Products

```bash
curl http://localhost:5000/products
```

### 3. Filter Products

```bash
# Filter by category
curl "http://localhost:5000/products?category=Electronics"

# Filter by price range
curl "http://localhost:5000/products?min_price=100&max_price=500"
```

### 4. Create a New Product

```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse with long battery life",
    "price": 29.99,
    "category": "Electronics"
  }'
```

### 5. Get a Specific Product

```bash
curl http://localhost:5000/products/{product-id}
```

### 6. Update a Product

```bash
curl -X PUT http://localhost:5000/products/{product-id} \
  -H "Content-Type: application/json" \
  -d '{
    "price": 24.99,
    "description": "Updated description with special offer"
  }'
```

### 7. Delete a Product

```bash
curl -X DELETE http://localhost:5000/products/{product-id}
```

## Response Format

### Success Responses

**List Products:**
```json
{
  "products": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Laptop",
      "description": "High-performance laptop",
      "price": 999.99,
      "category": "Electronics",
      "created_at": "2024-01-15T10:00:00.000000",
      "updated_at": "2024-01-15T10:00:00.000000"
    }
  ],
  "total": 1
}
```

**Create/Update Product:**
```json
{
  "message": "Product created successfully",
  "product": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse",
    "price": 29.99,
    "category": "Electronics",
    "created_at": "2024-01-15T10:00:00.000000",
    "updated_at": "2024-01-15T10:00:00.000000"
  }
}
```

### Error Responses

**Validation Errors:**
```json
{
  "errors": [
    "'name' is required",
    "Price must be non-negative"
  ]
}
```

**Not Found:**
```json
{
  "error": "Product not found"
}
```

## Validation Rules

- **Name**: Required, maximum 100 characters
- **Description**: Required, maximum 500 characters  
- **Price**: Required, must be a non-negative number
- **Category**: Optional, no length limit

## Sample Data

The API comes pre-loaded with these sample products:

1. **Laptop** - High-performance laptop for development ($999.99, Electronics)
2. **Coffee Mug** - Ceramic coffee mug with company logo ($12.50, Office Supplies)
3. **Desk Chair** - Ergonomic office chair with lumbar support ($299.00, Furniture)

## Testing the API

### Automated Test Script

A comprehensive test script is provided to verify all API functionality:

```bash
# Start the server in one terminal
python app.py

# Run tests in another terminal (after installing requests)
pip install requests
python test_api.py
```

The test script will:
- Test all CRUD operations
- Verify input validation
- Test filtering functionality
- Check error handling
- Clean up test data

### Manual Testing

You can also test the API manually using the curl examples provided above or any HTTP client like Postman, Insomnia, or HTTPie.

## Error Handling

The API includes comprehensive error handling for:

- **400 Bad Request**: Invalid input data, validation errors
- **404 Not Found**: Product not found, invalid endpoints
- **405 Method Not Allowed**: HTTP method not supported for endpoint
- **500 Internal Server Error**: Unexpected server errors

## Development Notes

- **In-Memory Storage**: All data is stored in memory and will be lost when the server restarts
- **Sample Data**: The server automatically loads sample products on startup
- **Debug Mode**: The server runs in debug mode by default for development
- **Host/Port**: Configured to run on all interfaces (`0.0.0.0`) port 5000

## Production Considerations

For production use, consider:

- Replace in-memory storage with a persistent database (PostgreSQL, MySQL, etc.)
- Add authentication and authorization
- Implement proper logging
- Add rate limiting
- Use environment variables for configuration
- Set up proper CORS if needed for web frontend
- Disable debug mode
- Add comprehensive unit and integration tests