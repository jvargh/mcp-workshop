from flask import jsonify
from marshmallow import ValidationError

def success_response(data=None, message="Success", status_code=200):
    """Create a standardized success response."""
    response = {
        'status': 'success',
        'message': message
    }
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code

def error_response(message="An error occurred", errors=None, status_code=400):
    """Create a standardized error response."""
    response = {
        'status': 'error',
        'message': message
    }
    if errors:
        response['errors'] = errors
    
    return jsonify(response), status_code

def validation_error_response(validation_error):
    """Create a response for validation errors."""
    return error_response(
        message="Validation error",
        errors=validation_error.messages,
        status_code=400
    )

def paginated_response(items, page, per_page, total, endpoint=None, **kwargs):
    """Create a paginated response."""
    has_prev = page > 1
    has_next = page < (total + per_page - 1) // per_page
    
    pagination_info = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': (total + per_page - 1) // per_page,
        'has_prev': has_prev,
        'has_next': has_next
    }
    
    # Add navigation URLs if endpoint is provided
    if endpoint:
        from flask import url_for
        pagination_info['prev_url'] = url_for(endpoint, page=page-1, per_page=per_page, **kwargs) if has_prev else None
        pagination_info['next_url'] = url_for(endpoint, page=page+1, per_page=per_page, **kwargs) if has_next else None
    
    return success_response(
        data={
            'items': items,
            'pagination': pagination_info
        }
    )

def not_found_response(resource="Resource"):
    """Create a not found response."""
    return error_response(
        message=f"{resource} not found",
        status_code=404
    )

def created_response(data, message="Resource created successfully"):
    """Create a created response."""
    return success_response(data=data, message=message, status_code=201)

def updated_response(data, message="Resource updated successfully"):
    """Create an updated response."""
    return success_response(data=data, message=message, status_code=200)

def deleted_response(message="Resource deleted successfully"):
    """Create a deleted response."""
    return success_response(message=message, status_code=200)