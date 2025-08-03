import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from decimal import Decimal

# Import Flask app components (these would be imported differently in a real app)
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class ProductMCPServer:
    """MCP Server for Flask Product Management API integration."""
    
    def __init__(self):
        self.mcp = FastMCP("Flask Product Management API")
        self.setup_tools()
    
    def setup_tools(self):
        """Set up MCP tools for product management operations."""
        
        @self.mcp.tool()
        def list_products(
            page: int = 1,
            per_page: int = 20,
            search: Optional[str] = None,
            category: Optional[str] = None,
            sort_by: str = "created_at",
            order: str = "desc"
        ) -> Dict[str, Any]:
            """
            List products with pagination, search, and filtering options.
            
            Args:
                page: Page number (default: 1)
                per_page: Items per page (default: 20, max: 100)
                search: Search term for name, description, or SKU
                category: Filter by product category
                sort_by: Sort field (name, price, created_at, updated_at)
                order: Sort order (asc, desc)
            
            Returns:
                Dictionary containing products list and pagination info
            """
            try:
                # This would call the Flask API endpoint
                # For demo purposes, returning mock data
                products = [
                    {
                        "id": 1,
                        "name": "Laptop",
                        "description": "High-performance laptop for developers",
                        "price": 999.99,
                        "category": "Electronics",
                        "stock_quantity": 10,
                        "sku": "LAP-001",
                        "created_at": "2024-01-01T10:00:00",
                        "updated_at": "2024-01-01T10:00:00"
                    }
                ]
                
                return {
                    "status": "success",
                    "data": {
                        "items": products,
                        "pagination": {
                            "page": page,
                            "per_page": per_page,
                            "total": len(products),
                            "pages": 1,
                            "has_prev": False,
                            "has_next": False
                        }
                    }
                }
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        def get_product(product_id: int) -> Dict[str, Any]:
            """
            Get a single product by ID.
            
            Args:
                product_id: The ID of the product to retrieve
            
            Returns:
                Dictionary containing product details
            """
            try:
                # Mock product data for demo
                if product_id == 1:
                    product = {
                        "id": 1,
                        "name": "Laptop",
                        "description": "High-performance laptop for developers",
                        "price": 999.99,
                        "category": "Electronics",
                        "stock_quantity": 10,
                        "sku": "LAP-001",
                        "created_at": "2024-01-01T10:00:00",
                        "updated_at": "2024-01-01T10:00:00"
                    }
                    return {
                        "status": "success",
                        "data": product,
                        "message": "Product retrieved successfully"
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Product not found"
                    }
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        def create_product(
            name: str,
            price: float,
            category: str,
            sku: str,
            description: Optional[str] = None,
            stock_quantity: int = 0
        ) -> Dict[str, Any]:
            """
            Create a new product.
            
            Args:
                name: Product name (required, max 100 chars)
                price: Product price (required, must be positive)
                category: Product category (required)
                sku: Stock Keeping Unit (required, must be unique)
                description: Product description (optional)
                stock_quantity: Initial stock quantity (default: 0)
            
            Returns:
                Dictionary containing created product details
            """
            try:
                # Validate required fields
                if not name or len(name) > 100:
                    return {
                        "status": "error",
                        "message": "Invalid name: must be 1-100 characters"
                    }
                
                if price <= 0:
                    return {
                        "status": "error",
                        "message": "Price must be greater than 0"
                    }
                
                if not category or len(category) > 50:
                    return {
                        "status": "error",
                        "message": "Invalid category: must be 1-50 characters"
                    }
                
                if not sku or len(sku) > 50:
                    return {
                        "status": "error",
                        "message": "Invalid SKU: must be 1-50 characters"
                    }
                
                if stock_quantity < 0:
                    return {
                        "status": "error",
                        "message": "Stock quantity must be non-negative"
                    }
                
                # Mock created product for demo
                product = {
                    "id": 999,  # Mock ID
                    "name": name,
                    "description": description,
                    "price": price,
                    "category": category,
                    "stock_quantity": stock_quantity,
                    "sku": sku,
                    "created_at": "2024-01-01T10:00:00",
                    "updated_at": "2024-01-01T10:00:00"
                }
                
                return {
                    "status": "success",
                    "data": product,
                    "message": "Product created successfully"
                }
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        def update_product(
            product_id: int,
            name: Optional[str] = None,
            price: Optional[float] = None,
            category: Optional[str] = None,
            sku: Optional[str] = None,
            description: Optional[str] = None,
            stock_quantity: Optional[int] = None
        ) -> Dict[str, Any]:
            """
            Update an existing product.
            
            Args:
                product_id: The ID of the product to update
                name: New product name (optional)
                price: New product price (optional)
                category: New product category (optional)
                sku: New SKU (optional)
                description: New product description (optional)
                stock_quantity: New stock quantity (optional)
            
            Returns:
                Dictionary containing updated product details
            """
            try:
                # Validate inputs
                if name is not None and (not name or len(name) > 100):
                    return {
                        "status": "error",
                        "message": "Invalid name: must be 1-100 characters"
                    }
                
                if price is not None and price <= 0:
                    return {
                        "status": "error",
                        "message": "Price must be greater than 0"
                    }
                
                if category is not None and (not category or len(category) > 50):
                    return {
                        "status": "error",
                        "message": "Invalid category: must be 1-50 characters"
                    }
                
                if sku is not None and (not sku or len(sku) > 50):
                    return {
                        "status": "error",
                        "message": "Invalid SKU: must be 1-50 characters"
                    }
                
                if stock_quantity is not None and stock_quantity < 0:
                    return {
                        "status": "error",
                        "message": "Stock quantity must be non-negative"
                    }
                
                # Mock updated product for demo
                if product_id == 1:
                    product = {
                        "id": product_id,
                        "name": name or "Laptop",
                        "description": description or "High-performance laptop for developers",
                        "price": price or 999.99,
                        "category": category or "Electronics",
                        "stock_quantity": stock_quantity if stock_quantity is not None else 10,
                        "sku": sku or "LAP-001",
                        "created_at": "2024-01-01T10:00:00",
                        "updated_at": "2024-01-01T10:30:00"
                    }
                    
                    return {
                        "status": "success",
                        "data": product,
                        "message": "Product updated successfully"
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Product not found"
                    }
            
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        def delete_product(product_id: int) -> Dict[str, Any]:
            """
            Delete a product by ID.
            
            Args:
                product_id: The ID of the product to delete
            
            Returns:
                Dictionary containing deletion status
            """
            try:
                # Mock deletion for demo
                if product_id == 1:
                    return {
                        "status": "success",
                        "message": "Product deleted successfully"
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Product not found"
                    }
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        def search_products(
            query: str,
            page: int = 1,
            per_page: int = 20,
            sort_by: str = "created_at",
            order: str = "desc"
        ) -> Dict[str, Any]:
            """
            Search products by name, description, or SKU.
            
            Args:
                query: Search term
                page: Page number (default: 1)
                per_page: Items per page (default: 20)
                sort_by: Sort field (name, price, created_at, updated_at)
                order: Sort order (asc, desc)
            
            Returns:
                Dictionary containing search results and pagination info
            """
            try:
                if not query.strip():
                    return {
                        "status": "error",
                        "message": "Search query is required"
                    }
                
                # Mock search results for demo
                products = [
                    {
                        "id": 1,
                        "name": "Laptop",
                        "description": "High-performance laptop for developers",
                        "price": 999.99,
                        "category": "Electronics",
                        "stock_quantity": 10,
                        "sku": "LAP-001",
                        "created_at": "2024-01-01T10:00:00",
                        "updated_at": "2024-01-01T10:00:00"
                    }
                ] if "laptop" in query.lower() else []
                
                return {
                    "status": "success",
                    "data": {
                        "items": products,
                        "pagination": {
                            "page": page,
                            "per_page": per_page,
                            "total": len(products),
                            "pages": 1 if products else 0,
                            "has_prev": False,
                            "has_next": False
                        }
                    }
                }
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        def get_products_by_category(
            category: str,
            page: int = 1,
            per_page: int = 20,
            sort_by: str = "created_at",
            order: str = "desc"
        ) -> Dict[str, Any]:
            """
            Get products filtered by category.
            
            Args:
                category: Product category to filter by
                page: Page number (default: 1)
                per_page: Items per page (default: 20)
                sort_by: Sort field (name, price, created_at, updated_at)
                order: Sort order (asc, desc)
            
            Returns:
                Dictionary containing products in the category and pagination info
            """
            try:
                # Mock category filtering for demo
                products = [
                    {
                        "id": 1,
                        "name": "Laptop",
                        "description": "High-performance laptop for developers",
                        "price": 999.99,
                        "category": "Electronics",
                        "stock_quantity": 10,
                        "sku": "LAP-001",
                        "created_at": "2024-01-01T10:00:00",
                        "updated_at": "2024-01-01T10:00:00"
                    }
                ] if category.lower() == "electronics" else []
                
                return {
                    "status": "success",
                    "data": {
                        "items": products,
                        "pagination": {
                            "page": page,
                            "per_page": per_page,
                            "total": len(products),
                            "pages": 1 if products else 0,
                            "has_prev": False,
                            "has_next": False
                        }
                    }
                }
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        @self.mcp.tool()
        def get_categories() -> Dict[str, Any]:
            """
            Get all unique product categories.
            
            Returns:
                Dictionary containing list of categories
            """
            try:
                # Mock categories for demo
                categories = ["Electronics", "Office Supplies", "Books", "Clothing"]
                
                return {
                    "status": "success",
                    "data": {"categories": categories},
                    "message": "Categories retrieved successfully"
                }
            except Exception as e:
                return {"status": "error", "message": str(e)}
    
    def run(self):
        """Run the MCP server."""
        print("🚀 Starting Flask Product Management MCP Server...")
        print("Available tools:")
        print("- list_products: List products with pagination and filtering")
        print("- get_product: Get a single product by ID")
        print("- create_product: Create a new product")
        print("- update_product: Update an existing product")
        print("- delete_product: Delete a product")
        print("- search_products: Search products by name, description, or SKU")
        print("- get_products_by_category: Get products by category")
        print("- get_categories: Get all product categories")
        print()
        self.mcp.run()

if __name__ == "__main__":
    server = ProductMCPServer()
    server.run()