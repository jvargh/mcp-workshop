import pytest
import json
from app import create_app
from models.product import db, Product

@pytest.fixture
def app():
    """Create and configure a test app."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def sample_product():
    """Create a sample product for testing."""
    return {
        'name': 'Test Laptop',
        'description': 'A high-performance test laptop',
        'price': 999.99,
        'category': 'Electronics',
        'stock_quantity': 5,
        'sku': 'TEST-LAP-001'
    }

class TestProductAPI:
    """Test cases for Product API endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_api_info(self, client):
        """Test API info endpoint."""
        response = client.get('/api')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'name' in data
        assert 'version' in data
    
    def test_create_product(self, client, sample_product):
        """Test creating a new product."""
        response = client.post(
            '/api/products',
            data=json.dumps(sample_product),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == sample_product['name']
        assert data['data']['sku'] == sample_product['sku']
    
    def test_create_product_validation_error(self, client):
        """Test creating product with validation errors."""
        invalid_product = {
            'name': '',  # Empty name should fail validation
            'price': -10,  # Negative price should fail
            'category': '',  # Empty category should fail
            'sku': ''  # Empty SKU should fail
        }
        
        response = client.post(
            '/api/products',
            data=json.dumps(invalid_product),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'errors' in data
    
    def test_get_product(self, client, app, sample_product):
        """Test getting a single product."""
        # First create a product
        with app.app_context():
            product = Product.from_dict(sample_product)
            db.session.add(product)
            db.session.commit()
            product_id = product.id
        
        # Then retrieve it
        response = client.get(f'/api/products/{product_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == sample_product['name']
    
    def test_get_nonexistent_product(self, client):
        """Test getting a product that doesn't exist."""
        response = client.get('/api/products/99999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()
    
    def test_list_products_empty(self, client):
        """Test listing products when none exist."""
        response = client.get('/api/products')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['items'] == []
        assert data['data']['pagination']['total'] == 0
    
    def test_list_products_with_data(self, client, app, sample_product):
        """Test listing products with data."""
        # Create a product first
        with app.app_context():
            product = Product.from_dict(sample_product)
            db.session.add(product)
            db.session.commit()
        
        response = client.get('/api/products')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']['items']) == 1
        assert data['data']['pagination']['total'] == 1
    
    def test_update_product(self, client, app, sample_product):
        """Test updating a product."""
        # Create a product first
        with app.app_context():
            product = Product.from_dict(sample_product)
            db.session.add(product)
            db.session.commit()
            product_id = product.id
        
        # Update the product
        update_data = {'name': 'Updated Laptop', 'price': 1299.99}
        response = client.put(
            f'/api/products/{product_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == 'Updated Laptop'
        assert float(data['data']['price']) == 1299.99
    
    def test_delete_product(self, client, app, sample_product):
        """Test deleting a product."""
        # Create a product first
        with app.app_context():
            product = Product.from_dict(sample_product)
            db.session.add(product)
            db.session.commit()
            product_id = product.id
        
        # Delete the product
        response = client.delete(f'/api/products/{product_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'deleted' in data['message'].lower()
        
        # Verify it's gone
        response = client.get(f'/api/products/{product_id}')
        assert response.status_code == 404
    
    def test_search_products(self, client, app, sample_product):
        """Test searching products."""
        # Create a product first
        with app.app_context():
            product = Product.from_dict(sample_product)
            db.session.add(product)
            db.session.commit()
        
        # Search for the product
        response = client.get('/api/products/search?q=laptop')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']['items']) >= 1
        
        # Search with no results
        response = client.get('/api/products/search?q=nonexistent')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']['items']) == 0
    
    def test_get_products_by_category(self, client, app, sample_product):
        """Test getting products by category."""
        # Create a product first
        with app.app_context():
            product = Product.from_dict(sample_product)
            db.session.add(product)
            db.session.commit()
        
        # Get products by category
        response = client.get('/api/products/category/Electronics')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']['items']) >= 1
        
        # Get products from non-existent category
        response = client.get('/api/products/category/NonExistent')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']['items']) == 0
    
    def test_get_categories(self, client, app, sample_product):
        """Test getting all categories."""
        # Create a product first
        with app.app_context():
            product = Product.from_dict(sample_product)
            db.session.add(product)
            db.session.commit()
        
        response = client.get('/api/products/categories')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'Electronics' in data['data']['categories']