#!/usr/bin/env python3
"""
Simple test script to demonstrate Flask Products API functionality.
Run this after starting the Flask server with: python app.py
"""

import requests
import json
import sys

BASE_URL = 'http://localhost:5000'

def test_api():
    """Test all API endpoints"""
    print("🧪 Testing Flask Products API\n")
    
    # Test health check
    print("1. Testing health check...")
    try:
        response = requests.get(f'{BASE_URL}/health')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except requests.ConnectionError:
        print("   ❌ Failed to connect to server. Is it running on port 5000?")
        sys.exit(1)
    
    # Test list products
    print("2. Testing list products...")
    response = requests.get(f'{BASE_URL}/products')
    products = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Found {products['total']} products\n")
    
    # Test create product
    print("3. Testing create product...")
    new_product = {
        'name': 'Test Product',
        'description': 'A test product created by the test script',
        'price': 19.99,
        'category': 'Test'
    }
    response = requests.post(f'{BASE_URL}/products', json=new_product)
    created_product = response.json()
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        product_id = created_product['product']['id']
        print(f"   Created product with ID: {product_id}\n")
    else:
        print(f"   Error: {created_product}\n")
        return
    
    # Test get specific product
    print("4. Testing get specific product...")
    response = requests.get(f'{BASE_URL}/products/{product_id}')
    print(f"   Status: {response.status_code}")
    product = response.json()
    print(f"   Product name: {product['product']['name']}\n")
    
    # Test update product
    print("5. Testing update product...")
    update_data = {
        'price': 15.99,
        'description': 'Updated test product description'
    }
    response = requests.put(f'{BASE_URL}/products/{product_id}', json=update_data)
    print(f"   Status: {response.status_code}")
    updated_product = response.json()
    print(f"   Updated price: ${updated_product['product']['price']}\n")
    
    # Test filter products
    print("6. Testing filter products by category...")
    response = requests.get(f'{BASE_URL}/products?category=Electronics')
    products = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Electronics products: {products['total']}\n")
    
    # Test validation error
    print("7. Testing validation (should fail)...")
    invalid_product = {
        'name': '',
        'price': -10
    }
    response = requests.post(f'{BASE_URL}/products', json=invalid_product)
    print(f"   Status: {response.status_code}")
    if response.status_code == 400:
        errors = response.json()
        print(f"   Validation errors: {errors['errors']}\n")
    
    # Test delete product
    print("8. Testing delete product...")
    response = requests.delete(f'{BASE_URL}/products/{product_id}')
    print(f"   Status: {response.status_code}")
    deleted_product = response.json()
    print(f"   Deleted: {deleted_product['product']['name']}\n")
    
    # Test get deleted product (should fail)
    print("9. Testing get deleted product (should fail)...")
    response = requests.get(f'{BASE_URL}/products/{product_id}')
    print(f"   Status: {response.status_code}")
    if response.status_code == 404:
        print("   ✅ Product not found as expected\n")
    
    print("🎉 All tests completed successfully!")

if __name__ == '__main__':
    test_api()