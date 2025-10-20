from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity
from .utils import check_ownership

def roles_required(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role", "")
            if role not in allowed_roles:
                return jsonify({"error": "Not authorized"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

def ownership_required(resource_user_id_field):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role", "")
            current_user_id = int(get_jwt_identity())
            resource_owner_id = kwargs.get(resource_user_id_field)

            if resource_owner_id is None:
                return jsonify({"error": "Could not determine owner"}), 400

            if not check_ownership(current_user_id, resource_owner_id, role):
                return jsonify({"error": "Not authorized"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator