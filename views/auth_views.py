# views/auth_views.py

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from passlib.hash import bcrypt

from app import db
from models import User, UserCredentials
from schemas import RegisterSchema, LoginSchema, UserSchema


class UserRegisterAPI(MethodView):
    """
    Registro de usuario:
    POST /api/register
    Body: { "name", "email", "password", "role" }
    """

    def post(self):
        try:
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if User.query.filter_by(email=data['email']).first():
            return {"error": "Email en uso"}, 400

        new_user = User(name=data["name"], email=data['email'])
        db.session.add(new_user)
        db.session.flush()  # Necesario para obtener ID antes de commit

        password_hash = bcrypt.hash(data['password'])
        credenciales = UserCredentials(
            user_id=new_user.id,
            password_hash=password_hash,
            role=data.get('role', 'user')
        )
        db.session.add(credenciales)
        db.session.commit()

        return UserSchema().dump(new_user), 201


class AuthLoginAPI(MethodView):
    """
    Login de usuario:
    POST /api/login
    Body: { "email", "password" }
    Response: { "access_token": "..." }
    """

    def post(self):
        try:
            data = LoginSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.credential:
            return {"errors": {"credentials": ["Inválidas"]}}, 401

        if not bcrypt.verify(data["password"], user.credential.password_hash):
            return {"errors": {"credentials": ["Inválidas"]}}, 401

        token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "email": user.email,
                "role": user.credential.role
            }
        )

        return {"access_token": token}, 200
