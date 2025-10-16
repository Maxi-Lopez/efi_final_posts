# app/utils.py

from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def roles_required(*roles):
    """
    Decorador para verificar si el rol del usuario está permitido
    Uso:
    @roles_required("admin", "moderator")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role", "")
            if user_role not in roles:
                return jsonify({"error": "No autorizado"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def check_ownership(user_id, resource_owner_id, role=None):
    """
    Verifica si el usuario es dueño del recurso
    - Si role es "admin", siempre devuelve True
    - Si user_id == resource_owner_id, devuelve True
    """
    if role == "admin":
        return True
    return user_id == resource_owner_id


def handle_validation_error(err):
    """
    Helper para devolver errores de Marshmallow de forma JSON
    """
    return jsonify({"errors": err.messages}), 400
