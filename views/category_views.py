# views/category_views.py

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app import db
from models import Category
from schemas import CategorySchema
from decorators import roles_required


class CategoryAPI(MethodView):
    """
    GET /api/categories          -> público
    POST /api/categories         -> moderator/admin
    """

    def get(self):
        categories = Category.query.filter_by(is_active=True).all()
        return CategorySchema(many=True).dump(categories), 200

    @jwt_required()
    @roles_required("moderator", "admin")
    def post(self):
        try:
            data = CategorySchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if Category.query.filter_by(nombre=data['nombre']).first():
            return {"error": "Categoría ya existe"}, 400

        new_category = Category(nombre=data['nombre'])
        db.session.add(new_category)
        db.session.commit()

        return CategorySchema().dump(new_category), 201


class CategoryDetailAPI(MethodView):
    """
    GET /api/categories/<id>    -> público
    PUT /api/categories/<id>    -> moderator/admin
    DELETE /api/categories/<id> -> admin
    """

    def get(self, id):
        category = Category.query.get_or_404(id)
        return CategorySchema().dump(category), 200

    @jwt_required()
    @roles_required("moderator", "admin")
    def put(self, id):
        category = Category.query.get_or_404(id)
        try:
            data = CategorySchema(partial=True).load(request.json)
            if 'nombre' in data:
                category.nombre = data['nombre']
            if 'is_active' in data:
                category.is_active = data['is_active']
            db.session.commit()
            return CategorySchema().dump(category), 200
        except ValidationError as err:
            return {"errors": err.messages}, 400

    @jwt_required()
    @roles_required("admin")
    def delete(self, id):
        category = Category.query.get_or_404(id)
        try:
            category.is_active = False  # soft delete
            db.session.commit()
            return {"message": "Categoría desactivada"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
