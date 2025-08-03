import pytest
import json
from decimal import Decimal
from models.product import Product

class TestProduct:
    """Test cases for Product model."""
    
    def test_product_creation(self):
        """Test creating a product instance."""
        product = Product(
            name="Test Product",
            description="A test product",
            price=Decimal('29.99'),
            category="Test Category",
            stock_quantity=10,
            sku="TEST-001"
        )
        
        assert product.name == "Test Product"
        assert product.description == "A test product"
        assert product.price == Decimal('29.99')
        assert product.category == "Test Category"
        assert product.stock_quantity == 10
        assert product.sku == "TEST-001"
    
    def test_product_to_dict(self):
        """Test converting product to dictionary."""
        product = Product(
            name="Test Product",
            description="A test product",
            price=Decimal('29.99'),
            category="Test Category",
            stock_quantity=10,
            sku="TEST-001"
        )
        
        product_dict = product.to_dict()
        
        assert product_dict['name'] == "Test Product"
        assert product_dict['description'] == "A test product"
        assert product_dict['price'] == 29.99
        assert product_dict['category'] == "Test Category"
        assert product_dict['stock_quantity'] == 10
        assert product_dict['sku'] == "TEST-001"
    
    def test_product_from_dict(self):
        """Test creating product from dictionary."""
        data = {
            'name': 'Test Product',
            'description': 'A test product',
            'price': 29.99,
            'category': 'Test Category',
            'stock_quantity': 10,
            'sku': 'TEST-001'
        }
        
        product = Product.from_dict(data)
        
        assert product.name == "Test Product"
        assert product.description == "A test product"
        assert product.price == 29.99
        assert product.category == "Test Category"
        assert product.stock_quantity == 10
        assert product.sku == "TEST-001"
    
    def test_product_repr(self):
        """Test product string representation."""
        product = Product(
            name="Test Product",
            sku="TEST-001"
        )
        
        expected = "<Product Test Product (SKU: TEST-001)>"
        assert repr(product) == expected