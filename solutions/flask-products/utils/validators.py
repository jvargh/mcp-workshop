from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from flask import current_app

class ProductSchema(Schema):
    """Schema for validating product data."""
    
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Product name is required.'}
    )
    description = fields.String(
        allow_none=True,
        validate=validate.Length(max=1000)
    )
    price = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0.01),
        error_messages={
            'required': 'Price is required.',
            'invalid': 'Price must be a valid decimal number.'
        }
    )
    category = fields.String(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={'required': 'Category is required.'}
    )
    stock_quantity = fields.Integer(
        load_default=0,
        validate=validate.Range(min=0),
        error_messages={'invalid': 'Stock quantity must be a non-negative integer.'}
    )
    sku = fields.String(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={'required': 'SKU is required.'}
    )
    created_at = fields.DateTime(dump_only=True, format='iso')
    updated_at = fields.DateTime(dump_only=True, format='iso')
    
    @validates_schema
    def validate_product(self, data, **kwargs):
        """Additional validation logic."""
        if 'price' in data and data['price'] <= 0:
            raise ValidationError('Price must be greater than 0.', 'price')

class ProductUpdateSchema(ProductSchema):
    """Schema for updating products - all fields optional except constraints."""
    
    name = fields.String(
        validate=validate.Length(min=1, max=100),
        allow_none=True
    )
    price = fields.Decimal(
        places=2,
        validate=validate.Range(min=0.01),
        allow_none=True
    )
    category = fields.String(
        validate=validate.Length(min=1, max=50),
        allow_none=True
    )
    sku = fields.String(
        validate=validate.Length(min=1, max=50),
        allow_none=True
    )

class ProductQuerySchema(Schema):
    """Schema for validating query parameters."""
    
    page = fields.Integer(
        load_default=1,
        validate=validate.Range(min=1)
    )
    per_page = fields.Integer(
        load_default=20,
        validate=validate.Range(min=1, max=100)
    )
    q = fields.String(
        validate=validate.Length(min=1, max=100),
        allow_none=True
    )
    category = fields.String(
        validate=validate.Length(min=1, max=50),
        allow_none=True
    )
    sort_by = fields.String(
        load_default='created_at',
        validate=validate.OneOf(['name', 'price', 'created_at', 'updated_at'])
    )
    order = fields.String(
        load_default='desc',
        validate=validate.OneOf(['asc', 'desc'])
    )