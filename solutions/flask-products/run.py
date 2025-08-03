#!/usr/bin/env python3
"""
Flask Products API - Entry Point

This script runs the Flask Product Management API server.
"""

import os
from app import create_app

if __name__ == '__main__':
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create the Flask app
    app = create_app(config_name)
    
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = config_name == 'development'
    
    print(f"🚀 Starting Flask Product Management API...")
    print(f"📍 Environment: {config_name}")
    print(f"🌐 Running on http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    
    # Initialize database tables
    with app.app_context():
        from models.product import db
        db.create_all()
        print("✅ Database tables initialized")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug
    )