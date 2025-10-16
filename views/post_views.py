# views/post_views.py

from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError

from app import db
from models import Post, Category
from schemas import PostSchema
from decorators import roles_required
from utils import check_ownership


class PostAPI(MethodView):
    """
    GET /api/posts         -> público
    POST /api/posts        -> user+, moderator, admin
    """

    def get(self):
        posts = Post.query.filter_by(is_published=True).all()
        return PostSchema(many=True).dump(posts), 200

    @jwt_required()
    def post(self):
        try:
            data = PostSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        # si viene categoría
        category = None
        if 'category_id' in data:
            category = Category.query.get(data['category_id'])
            if not category:
                return {"error": "Categoría no encontrada"}, 404

        new_post = Post(
            titulo=data['titulo'],
            contenido=data['contenido'],
            author_id=int(get_jwt_identity()),
            category_id=category.id if category else None
        )
        db.session.add(new_post)
        db.session.commit()

        return PostSchema().dump(new_post), 201


class PostDetailAPI(MethodView):
    """
    GET    /api/posts/<id>   -> público
    PUT    /api/posts/<id>   -> autor o admin
    DELETE /api/posts/<id>   -> autor o admin
    """

    def get(self, id):
        post = Post.query.get_or_404(id)
        if not post.is_published:
            return {"error": "Post no disponible"}, 404
        return PostSchema().dump(post), 200

    @jwt_required()
    def put(self, id):
        post = Post.query.get_or_404(id)
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()

        # solo el autor o admin
        if not check_ownership(current_user_id, post.author_id) and claims['role'] != 'admin':
            return {"error": "No autorizado"}, 403

        try:
            data = PostSchema(partial=True).load(request.json)
            if 'titulo' in data:
                post.titulo = data['titulo']
            if 'contenido' in data:
                post.contenido = data['contenido']
            if 'is_published' in data and claims['role'] in ['admin', 'moderator']:
                post.is_published = data['is_published']
            if 'category_id' in data:
                category = Category.query.get(data['category_id'])
                if not category:
                    return {"error": "Categoría no encontrada"}, 404
                post.category_id = category.id

            db.session.commit()
            return PostSchema().dump(post), 200
        except ValidationError as err:
            return {"errors": err.messages}, 400

    @jwt_required()
    def delete(self, id):
        post = Post.query.get_or_404(id)
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()

        # solo el autor o admin
        if not check_ownership(current_user_id, post.author_id) and claims['role'] != 'admin':
            return {"error": "No autorizado"}, 403

        post.is_published = False  # soft delete
        db.session.commit()
        return {"message": "Post eliminado"}, 200
