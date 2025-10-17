from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity
from .utils import check_ownership



def roles_required(*allowed_roles):
    """
    Decorador para verificar que el usuario tenga uno de los roles permitidos.
    Uso:
        @roles_required("admin", "moderator")
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role", "")
            if role not in allowed_roles:
                return jsonify({"error": "No autorizado"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


def ownership_required(resource_user_id_field):
    """
    Verifica que el usuario sea dueño del recurso o sea admin.
    - resource_user_id_field: nombre del parámetro que contiene el user_id del recurso
    Ejemplo:
        @ownership_required("autor_id")
        def put(self, id):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role", "")
            current_user_id = int(get_jwt_identity())
            resource_owner_id = kwargs.get(resource_user_id_field)

            if resource_owner_id is None:
                return jsonify({"error": "No se pudo determinar el propietario"}), 400

            if not check_ownership(current_user_id, resource_owner_id, role):
                return jsonify({"error": "No autorizado"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
