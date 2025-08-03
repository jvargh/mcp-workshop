import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from models.product import db
from routes.products import products_bp
from utils.responses import error_response
from marshmallow import ValidationError
from config import config

migrate = Migrate()

def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    app.register_blueprint(products_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return error_response(
            message="Validation error",
            errors=e.messages,
            status_code=400
        )
    
    @app.errorhandler(404)
    def handle_not_found(e):
        return error_response(
            message="Endpoint not found",
            status_code=404
        )
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        return error_response(
            message="Internal server error",
            status_code=500
        )
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Flask Product API is running'}, 200
    
    # API info endpoint
    @app.route('/api')
    def api_info():
        return {
            'name': 'Flask Product Management API',
            'version': '1.0.0',
            'description': 'RESTful API for managing products with MCP integration',
            'endpoints': {
                'products': '/api/products',
                'health': '/health'
            }
        }, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Optional: Add some seed data for development
        if app.config['DEBUG'] and not db.session.query(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")).fetchone():
            from models.product import Product
            
            sample_products = [
                Product(
                    name="Laptop",
                    description="High-performance laptop for developers",
                    price=999.99,
                    category="Electronics",
                    stock_quantity=10,
                    sku="LAP-001"
                ),
                Product(
                    name="Coffee Mug",
                    description="Ceramic coffee mug with company logo",
                    price=15.99,
                    category="Office Supplies",
                    stock_quantity=50,
                    sku="MUG-001"
                ),
                Product(
                    name="Wireless Mouse",
                    description="Ergonomic wireless mouse",
                    price=29.99,
                    category="Electronics",
                    stock_quantity=25,
                    sku="MOU-001"
                )
            ]
            
            for product in sample_products:
                db.session.add(product)
            
            try:
                db.session.commit()
                print("Sample products added to database")
            except Exception as e:
                db.session.rollback()
                print(f"Error adding sample products: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)