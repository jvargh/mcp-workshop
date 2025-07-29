from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory storage for products
products = {}

class Product:
    def __init__(self, name, description, price, category=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def update(self, name=None, description=None, price=None, category=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if price is not None:
            self.price = price
        if category is not None:
            self.category = category
        self.updated_at = datetime.now().isoformat()

def validate_product_data(data, required_fields=None):
    """Validate product data and return errors if any"""
    errors = []
    
    if required_fields is None:
        required_fields = ['name', 'description', 'price']
    
    # Check required fields
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"'{field}' is required")
    
    # Validate price
    if 'price' in data and data['price'] is not None:
        try:
            price = float(data['price'])
            if price < 0:
                errors.append("Price must be non-negative")
        except (ValueError, TypeError):
            errors.append("Price must be a valid number")
    
    # Validate name length
    if 'name' in data and data['name'] and len(data['name']) > 100:
        errors.append("Name must be 100 characters or less")
    
    # Validate description length
    if 'description' in data and data['description'] and len(data['description']) > 500:
        errors.append("Description must be 500 characters or less")
    
    return errors

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/products', methods=['GET'])
def list_products():
    """List all products with optional filtering"""
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    filtered_products = list(products.values())
    
    # Apply filters
    if category:
        filtered_products = [p for p in filtered_products if p.category and p.category.lower() == category.lower()]
    
    if min_price:
        try:
            min_price = float(min_price)
            filtered_products = [p for p in filtered_products if p.price >= min_price]
        except ValueError:
            return jsonify({'error': 'Invalid min_price format'}), 400
    
    if max_price:
        try:
            max_price = float(max_price)
            filtered_products = [p for p in filtered_products if p.price <= max_price]
        except ValueError:
            return jsonify({'error': 'Invalid max_price format'}), 400
    
    return jsonify({
        'products': [p.to_dict() for p in filtered_products],
        'total': len(filtered_products)
    })

@app.route('/products', methods=['POST'])
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate input data
        errors = validate_product_data(data)
        if errors:
            return jsonify({'errors': errors}), 400
        
        # Create new product
        product = Product(
            name=data['name'],
            description=data['description'],
            price=float(data['price']),
            category=data.get('category')
        )
        
        products[product.id] = product
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    if product_id not in products:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({'product': products[product_id].to_dict()})

@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product"""
    if product_id not in products:
        return jsonify({'error': 'Product not found'}), 404
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate input data (no required fields for update)
        errors = validate_product_data(data, required_fields=[])
        if errors:
            return jsonify({'errors': errors}), 400
        
        # Update product
        product = products[product_id]
        product.update(
            name=data.get('name'),
            description=data.get('description'),
            price=float(data['price']) if 'price' in data else None,
            category=data.get('category')
        )
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    if product_id not in products:
        return jsonify({'error': 'Product not found'}), 404
    
    deleted_product = products.pop(product_id)
    
    return jsonify({
        'message': 'Product deleted successfully',
        'product': deleted_product.to_dict()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize with some sample data
def init_sample_data():
    """Initialize the API with some sample products"""
    sample_products = [
        {
            'name': 'Laptop',
            'description': 'High-performance laptop for development',
            'price': 999.99,
            'category': 'Electronics'
        },
        {
            'name': 'Coffee Mug',
            'description': 'Ceramic coffee mug with company logo',
            'price': 12.50,
            'category': 'Office Supplies'
        },
        {
            'name': 'Desk Chair',
            'description': 'Ergonomic office chair with lumbar support',
            'price': 299.00,
            'category': 'Furniture'
        }
    ]
    
    for product_data in sample_products:
        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            category=product_data['category']
        )
        products[product.id] = product

if __name__ == '__main__':
    init_sample_data()
    print("Starting Flask Products API server...")
    print("Sample products have been loaded into memory.")
    app.run(debug=True, host='0.0.0.0', port=5000)