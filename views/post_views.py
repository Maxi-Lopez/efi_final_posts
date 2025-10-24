from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app import db
from models import Post, Category
from schemas import PostSchema
from decorators.decorators import roles_required, ownership_required

class PostAPI(MethodView):
    def get(self):
        """Cualquiera puede ver los posts"""
        posts = Post.query.filter_by(is_visible=True).all()
        return PostSchema(many=True).dump(posts), 200

    @jwt_required()
    def post(self):
        """Solo usuarios logueados pueden crear posts"""
        from flask_jwt_extended import get_jwt_identity
        user_id = int(get_jwt_identity())
        data = request.get_json()
        new_post = Post(
            title=data['title'],
            content=data['content'],
            author_id=user_id,
            is_visible=True
        )
        db.session.add(new_post)
        db.session.commit()
        return PostSchema().dump(new_post), 201

class PostDetailAPI(MethodView):
    def get(self, id):
        post = Post.query.get_or_404(id)
        if not post.is_published:
            return {"error": "Post not available"}, 404
        return PostSchema().dump(post), 200

    @jwt_required()
    @ownership_required("id")  # autor o admin/moderator
    def put(self, id):
        post = Post.query.get_or_404(id)
        from flask_jwt_extended import get_jwt_identity, get_jwt
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()

        try:
            data = PostSchema(partial=True).load(request.json)
            if 'title' in data:
                post.title = data['title']
            if 'content' in data:
                post.content = data['content']
            # Solo admin o moderator puede publicar
            if 'is_published' in data and claims['role'] in ['admin', 'moderator']:
                post.is_published = data['is_published']
            if 'category_id' in data:
                category = Category.query.get(data['category_id'])
                if not category:
                    return {"error": "Category not found"}, 404
                post.category_id = category.id

            db.session.commit()
            return PostSchema().dump(post), 200
        except ValidationError as err:
            return {"errors": err.messages}, 400

    @jwt_required()
    @ownership_required("id")
    def delete(self, id):
        """Eliminar post: autor o admin/moderator"""
        post = Post.query.get_or_404(id)
        post.is_published = False
        db.session.commit()
        return {"message": "Post deleted"}, 200
