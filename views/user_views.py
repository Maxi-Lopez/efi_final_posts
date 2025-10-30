from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, create_access_token
from marshmallow import ValidationError
import bcrypt

from app import db
from models import User, UserCredentials
from schemas import UserSchema, RegisterSchema, LoginSchema
from decorators.decorators import roles_required, ownership_required

class UserAPI(MethodView):
    @jwt_required()
    @roles_required("admin")
    def get(self):
        """Listar todos los usuarios (solo admin)"""
        users = User.query.all()
        return UserSchema(many=True).dump(users), 200

    def post(self):
        """Registro público de usuario con rol 'user'"""
        try:
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if User.query.filter_by(email=data['email']).first():
            return {"error": "Email already in use"}, 400

        requested_role = data.get('role', 'user')
        if requested_role != 'user':
            return {"error": "Only 'user' role can be assigned during registration"}, 400

        new_user = User(name=data["name"], email=data['email'])
        db.session.add(new_user)
        db.session.flush()

        password_hash = bcrypt.hash(data['password'])
        credentials = UserCredentials(
            user_id=new_user.id,
            password_hash=password_hash,
            role='user'
        )
        db.session.add(credentials)
        db.session.commit()

        return UserSchema().dump(new_user), 201


class UserDetailAPI(MethodView):
    @jwt_required()
    @ownership_required("id")  # Usuario puede ver su info o admin
    def get(self, id):
        user = User.query.get_or_404(id)
        return UserSchema().dump(user), 200

    @jwt_required()
    @ownership_required("id")  # Usuario puede modificar su info o admin
    def put(self, id):
        user = User.query.get_or_404(id)
        try:
            data = UserSchema(partial=True).load(request.json)
            if "name" in data:
                user.name = data["name"]
            if "email" in data:
                user.email = data["email"]
            db.session.commit()
            return UserSchema().dump(user), 200
        except ValidationError as err:
            return {"errors": err.messages}, 400

    @jwt_required()
    @roles_required("admin")  # Solo admin puede cambiar roles
    def patch(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()
        if not data or 'role' not in data:
            return {"error": "Role field is required"}, 400

        role = data['role']
        if role not in ["user", "moderator", "admin"]:
            return {"error": "Invalid role. Must be 'user', 'moderator' or 'admin'"}, 400

        if not hasattr(user, "credential") or not user.credential:
            return {"error": "User has no credentials"}, 400

        current_user_id = int(get_jwt_identity())
        if user.id == current_user_id and role != "admin":
            return {"error": "Cannot remove your own admin privileges"}, 400

        user.credential.role = role
        db.session.commit()
        return {
            "message": f"User role updated to {role}",
            "user": UserSchema().dump(user)
        }, 200

    @jwt_required()
    @roles_required("admin")  # Solo admin puede eliminar
    def delete(self, id):
        user = User.query.get_or_404(id)
        current_user_id = int(get_jwt_identity())
        if user.id == current_user_id:
            return {"error": "Cannot delete your own account"}, 400

        if hasattr(user, "credential") and user.credential:
            db.session.delete(user.credential)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200


class UserRegisterAPI(MethodView):
    def post(self):
        try:
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if User.query.filter_by(email=data['email']).first():
            return {"error": "Email already in use"}, 400

        requested_role = data.get('role', 'user')
        if requested_role != 'user':
            return {"error": "Only 'user' role can be assigned during registration"}, 400

        new_user = User(name=data["name"], email=data['email'])  # Sin role
        db.session.add(new_user)
        db.session.flush()

        password_bytes = data['password'].encode('utf-8')
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

        credentials = UserCredentials(
            user_id=new_user.id,
            password_hash=password_hash,
            role='user'  
        )
        db.session.add(credentials)
        db.session.commit()

        return UserSchema().dump(new_user), 201  

class AuthLoginAPI(MethodView):
    def post(self):
        try:
            data = LoginSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.credential:
            return {"errors": {"credentials": ["Invalid credentials"]}}, 401

        password_bytes = data["password"].encode('utf-8')
        stored_hash_bytes = user.credential.password_hash.encode('utf-8')

        if not bcrypt.checkpw(password_bytes, stored_hash_bytes):
            return {"errors": {"credentials": ["Invalid credentials"]}}, 401

        token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "email": user.email,
                "role": user.credential.role
            }
        )

        return {"access_token": token}, 200