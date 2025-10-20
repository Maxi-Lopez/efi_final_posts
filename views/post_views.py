from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError

from app import db
from models import Post, Category
from schemas import PostSchema
from decorators import roles_required, check_ownership

class PostAPI(MethodView):
    def get(self):
        posts = Post.query.filter_by(is_published=True).all()
        return PostSchema(many=True).dump(posts), 200

    @jwt_required()
    @roles_required("admin", "author")
    def post(self):
        try:
            data = PostSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        category = None

        if 'category_id' in data:
            category = Category.query.get(data['category_id'])
            if not category:
                return {"error": "Category not found"}, 404

        elif 'category_name' in data:
            category_name = data['category_name'].strip()
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()

        new_post = Post(
            title=data['title'],
            content=data['content'],
            author_id=int(get_jwt_identity()),
            category_id=category.id if category else None
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
    def put(self, id):
        post = Post.query.get_or_404(id)
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()

        if not check_ownership(current_user_id, post.author_id) and claims['role'] != 'admin':
            return {"error": "Not authorized"}, 403

        try:
            data = PostSchema(partial=True).load(request.json)
            if 'title' in data:
                post.title = data['title']
            if 'content' in data:
                post.content = data['content']
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
    def delete(self, id):
        post = Post.query.get_or_404(id)
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()

        if not check_ownership(current_user_id, post.author_id) and claims['role'] != 'admin':
            return {"error": "Not authorized"}, 403

        post.is_published = False
        db.session.commit()
        return {"message": "Post deleted"}, 200