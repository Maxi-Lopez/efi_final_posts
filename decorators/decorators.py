# src/decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from models import Post

# --------------------------------------
# 🔹 Verifica si el usuario tiene rol permitido
# --------------------------------------
def roles_required(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Solo verificar JWT y roles
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role", "")
            if role not in allowed_roles:
                return jsonify({"error": "Not authorized"}), 403
            return func(*args, **kwargs)
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
def ownership_required(resource_id_field):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Primero verificamos JWT
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role", "")
            current_user_id = int(get_jwt_identity())

            resource_id = kwargs.get(resource_id_field)
            if resource_id is None:
                return jsonify({"error": "Could not determine resource ID"}), 400

            # Buscar el post
            post = Post.query.get(resource_id)
            if not post:
                return jsonify({"error": "Post not found"}), 404

            # Solo admin, moderator o propietario puede continuar
            if role not in ["admin", "moderator"] and post.author_id != current_user_id:
                return jsonify({"error": "Not authorized"}), 403

            # Ejecutar la función, cualquier otro error sube normalmente
            return func(*args, **kwargs)

        return wrapper
    return decorator
