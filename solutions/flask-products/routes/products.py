from flask import Blueprint, request, current_app
from sqlalchemy import or_, and_
from marshmallow import ValidationError
from models.product import db, Product
from utils.validators import ProductSchema, ProductUpdateSchema, ProductQuerySchema
from utils.responses import (
    success_response, error_response, validation_error_response,
    paginated_response, not_found_response, created_response,
    updated_response, deleted_response
)

products_bp = Blueprint('products', __name__)

# Initialize schemas
product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)
product_update_schema = ProductUpdateSchema()
query_schema = ProductQuerySchema()

@products_bp.route('/products', methods=['GET'])
def list_products():
    """List all products with pagination, search, and filtering."""
    try:
        # Validate query parameters
        query_params = query_schema.load(request.args)
    except ValidationError as e:
        return validation_error_response(e)
    
    # Build query
    query = Product.query
    
    # Apply search filter
    if query_params.get('q'):
        search_term = query_params['q']
        query = query.filter(or_(
            Product.name.contains(search_term),
            Product.description.contains(search_term),
            Product.sku.contains(search_term)
        ))
    
    # Apply category filter
    if query_params.get('category'):
        query = query.filter(Product.category == query_params['category'])
    
    # Apply sorting
    sort_by = query_params.get('sort_by', 'created_at')
    order = query_params.get('order', 'desc')
    
    if hasattr(Product, sort_by):
        sort_column = getattr(Product, sort_by)
        if order == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    
    # Paginate results
    page = query_params.get('page', 1)
    per_page = query_params.get('per_page', current_app.config.get('PRODUCTS_PER_PAGE', 20))
    
    try:
        paginated_products = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        products = product_list_schema.dump(paginated_products.items)
        
        return paginated_response(
            items=products,
            page=page,
            per_page=per_page,
            total=paginated_products.total,
            endpoint='products.list_products',
            **{k: v for k, v in query_params.items() if k not in ['page', 'per_page']}
        )
    
    except Exception as e:
        current_app.logger.error(f"Error listing products: {e}")
        return error_response("Failed to retrieve products", status_code=500)

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID."""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return not_found_response("Product")
        
        return success_response(
            data=product_schema.dump(product),
            message="Product retrieved successfully"
        )
    
    except Exception as e:
        current_app.logger.error(f"Error retrieving product {product_id}: {e}")
        return error_response("Failed to retrieve product", status_code=500)

@products_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product."""
    try:
        # Validate input data
        product_data = product_schema.load(request.get_json() or {})
    except ValidationError as e:
        return validation_error_response(e)
    
    try:
        # Check if SKU already exists
        existing_product = Product.query.filter_by(sku=product_data['sku']).first()
        if existing_product:
            return error_response(
                message="Product with this SKU already exists",
                errors={'sku': ['SKU must be unique']},
                status_code=409
            )
        
        # Create new product
        product = Product.from_dict(product_data)
        db.session.add(product)
        db.session.commit()
        
        return created_response(
            data=product_schema.dump(product),
            message="Product created successfully"
        )
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating product: {e}")
        return error_response("Failed to create product", status_code=500)

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product."""
    try:
        # Validate input data
        update_data = product_update_schema.load(request.get_json() or {})
    except ValidationError as e:
        return validation_error_response(e)
    
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return not_found_response("Product")
        
        # Check SKU uniqueness if being updated
        if 'sku' in update_data and update_data['sku'] != product.sku:
            existing_product = Product.query.filter_by(sku=update_data['sku']).first()
            if existing_product:
                return error_response(
                    message="Product with this SKU already exists",
                    errors={'sku': ['SKU must be unique']},
                    status_code=409
                )
        
        # Update product fields
        for field, value in update_data.items():
            if value is not None:  # Only update fields that are provided
                setattr(product, field, value)
        
        db.session.commit()
        
        return updated_response(
            data=product_schema.dump(product),
            message="Product updated successfully"
        )
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating product {product_id}: {e}")
        return error_response("Failed to update product", status_code=500)

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product."""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return not_found_response("Product")
        
        db.session.delete(product)
        db.session.commit()
        
        return deleted_response("Product deleted successfully")
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting product {product_id}: {e}")
        return error_response("Failed to delete product", status_code=500)

@products_bp.route('/products/search', methods=['GET'])
def search_products():
    """Search products by name, description, or SKU."""
    search_term = request.args.get('q', '').strip()
    
    if not search_term:
        return error_response(
            message="Search term is required",
            errors={'q': ['Query parameter q is required']},
            status_code=400
        )
    
    try:
        # Validate other query parameters
        query_params = query_schema.load(request.args)
    except ValidationError as e:
        return validation_error_response(e)
    
    try:
        # Search across name, description, and SKU
        query = Product.query.filter(or_(
            Product.name.ilike(f'%{search_term}%'),
            Product.description.ilike(f'%{search_term}%'),
            Product.sku.ilike(f'%{search_term}%')
        ))
        
        # Apply sorting
        sort_by = query_params.get('sort_by', 'created_at')
        order = query_params.get('order', 'desc')
        
        if hasattr(Product, sort_by):
            sort_column = getattr(Product, sort_by)
            if order == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
        
        # Paginate results
        page = query_params.get('page', 1)
        per_page = query_params.get('per_page', current_app.config.get('PRODUCTS_PER_PAGE', 20))
        
        paginated_products = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        products = product_list_schema.dump(paginated_products.items)
        
        return paginated_response(
            items=products,
            page=page,
            per_page=per_page,
            total=paginated_products.total,
            endpoint='products.search_products',
            q=search_term,
            **{k: v for k, v in query_params.items() if k not in ['page', 'per_page', 'q']}
        )
    
    except Exception as e:
        current_app.logger.error(f"Error searching products: {e}")
        return error_response("Failed to search products", status_code=500)

@products_bp.route('/products/category/<string:category>', methods=['GET'])
def get_products_by_category(category):
    """Get products filtered by category."""
    try:
        # Validate query parameters
        query_params = query_schema.load(request.args)
    except ValidationError as e:
        return validation_error_response(e)
    
    try:
        # Query products by category
        query = Product.query.filter(Product.category == category)
        
        # Apply sorting
        sort_by = query_params.get('sort_by', 'created_at')
        order = query_params.get('order', 'desc')
        
        if hasattr(Product, sort_by):
            sort_column = getattr(Product, sort_by)
            if order == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
        
        # Paginate results
        page = query_params.get('page', 1)
        per_page = query_params.get('per_page', current_app.config.get('PRODUCTS_PER_PAGE', 20))
        
        paginated_products = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        products = product_list_schema.dump(paginated_products.items)
        
        return paginated_response(
            items=products,
            page=page,
            per_page=per_page,
            total=paginated_products.total,
            endpoint='products.get_products_by_category',
            category=category,
            **{k: v for k, v in query_params.items() if k not in ['page', 'per_page']}
        )
    
    except Exception as e:
        current_app.logger.error(f"Error retrieving products by category {category}: {e}")
        return error_response("Failed to retrieve products by category", status_code=500)

@products_bp.route('/products/categories', methods=['GET'])
def get_categories():
    """Get all unique product categories."""
    try:
        categories = db.session.query(Product.category).distinct().all()
        category_list = [category[0] for category in categories]
        
        return success_response(
            data={'categories': category_list},
            message="Categories retrieved successfully"
        )
    
    except Exception as e:
        current_app.logger.error(f"Error retrieving categories: {e}")
        return error_response("Failed to retrieve categories", status_code=500)