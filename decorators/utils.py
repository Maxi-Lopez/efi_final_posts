from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role", "")
            if user_role not in roles:
                return jsonify({"error": "Not authorized"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def check_ownership(user_id, resource_owner_id, role=None):
    if role == "admin":
        return True
    return user_id == resource_owner_id

def handle_validation_error(err):
    return jsonify({"errors": err.messages}), 400