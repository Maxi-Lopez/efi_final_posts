# src/decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

# --------------------------------------
# 🔹 Verifica si el usuario tiene rol permitido
# --------------------------------------
def roles_required(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                role = claims.get("role", "")
                if role not in allowed_roles:
                    return jsonify({"error": "Not authorized"}), 403
                return func(*args, **kwargs)
            except Exception as e:
                return jsonify({"error": "Invalid token"}), 401
        return wrapper
    return decorator

# --------------------------------------
# 🔹 Función de utilidad para verificar ownership
# --------------------------------------
def check_ownership(current_user_id, resource_owner_id, user_role=None):
    """
    Función auxiliar que puede ser usada directamente en las views.
    Devuelve True si el usuario es admin, moderator o es el propietario.
    """
    if user_role in ["admin", "moderator"]:
        return True
    return current_user_id == resource_owner_id

# --------------------------------------
# 🔹 Decorador para verificar ownership
# --------------------------------------
def ownership_required(resource_user_id_field):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                role = claims.get("role", "")
                current_user_id = int(get_jwt_identity())
                resource_owner_id = kwargs.get(resource_user_id_field)

                if resource_owner_id is None:
                    return jsonify({"error": "Could not determine owner"}), 400

                if not check_ownership(current_user_id, resource_owner_id, role):
                    return jsonify({"error": "Not authorized"}), 403

                return func(*args, **kwargs)
            except Exception as e:
                return jsonify({"error": "Invalid token"}), 401
        return wrapper
    return decorator