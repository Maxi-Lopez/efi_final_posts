from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, create_access_token
from marshmallow import ValidationError
from passlib.hash import bcrypt

from app import db
from models import User, UserCredentials
from schemas import UserSchema, RegisterSchema, LoginSchema
from decorators import roles_required, check_ownership

class UserAPI(MethodView):
    @jwt_required()
    @roles_required("admin")
    def get(self):
        users = User.query.all()
        return UserSchema(many=True).dump(users), 200

    def post(self):
        try:
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if User.query.filter_by(email=data['email']).first():
            return {"error": "Email already in use"}, 400

        new_user = User(name=data["name"], email=data['email'])
        db.session.add(new_user)
        db.session.flush()

        password_hash = bcrypt.hash(data['password'])
        credentials = UserCredentials(
            user_id=new_user.id,
            password_hash=password_hash,
            role=data['role']
        )
        db.session.add(credentials)
        db.session.commit()

        return UserSchema().dump(new_user), 201

class UserDetailAPI(MethodView):
    @jwt_required()
    def get(self, id):
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        if claims["role"] != "admin" and current_user_id != id:
            return {"error": "Not authorized"}, 403

        user = User.query.get_or_404(id)
        return UserSchema().dump(user), 200

    @jwt_required()
    def put(self, id):
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        if claims["role"] != "admin" and current_user_id != id:
            return {"error": "Not authorized"}, 403

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
    @roles_required("admin")
    def patch(self, id):
        user = User.query.get_or_404(id)
        try:
            role = request.json.get("role")
            if role not in ["user", "moderator", "admin"]:
                return {"error": "Invalid role"}, 400

            if not hasattr(user, "credential") or not user.credential:
                return {"error": "User has no credentials"}, 400

            user.credential.role = role
            db.session.commit()
            return {"message": f"Role changed to {role}"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @jwt_required()
    @roles_required("admin")
    def delete(self, id):
        user = User.query.get_or_404(id)
        try:
            if hasattr(user, "credential") and user.credential:
                db.session.delete(user.credential)
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

class AuthLoginAPI(MethodView):
    def post(self):
        try:
            data = LoginSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.credential:
            return {"errors": {"credentials": ["Invalid credentials"]}}, 401

        if not bcrypt.verify(data["password"], user.credential.password_hash):
            return {"errors": {"credentials": ["Invalid credentials"]}}, 401

        token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "email": user.email,
                "role": user.credential.role
            }
        )
        return {"access_token": token}, 200