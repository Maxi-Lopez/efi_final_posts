from app import db
from models import Category
from schemas import CategorySchema
from decorators.decorators import roles_required

from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

class CategoryAPI(MethodView):
    def get(self):
        categories = Category.query.filter_by(is_active=True).all()
        return CategorySchema(many=True).dump(categories), 200

    @jwt_required()
    def post(self):
        try:
            data = CategorySchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if Category.query.filter_by(name=data['name']).first():
            return {"error": "Category already exists"}, 400

        new_category = Category(name=data['name'])
        db.session.add(new_category)
        db.session.commit()
        return CategorySchema().dump(new_category), 201

class CategoryDetailAPI(MethodView):
    def get(self, id):
        category = Category.query.get_or_404(id)
        return CategorySchema().dump(category), 200

    @jwt_required()
    @roles_required("moderator", "admin")
    def put(self, id):
        category = Category.query.get_or_404(id)
        try:
            data = CategorySchema(partial=True).load(request.json)
            if 'name' in data:
                category.name = data['name']
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
        category.is_active = False
        db.session.commit()
        return {"message": "Category deactivated"}, 200
