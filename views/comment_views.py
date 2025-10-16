# views/comment_views.py

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError

from app import db
from models import Comment, Post
from schemas import CommentSchema
from decorators import roles_required
from utils import check_ownership


class CommentAPI(MethodView):
    """
    GET /api/posts/<post_id>/comments  -> público
    POST /api/posts/<post_id>/comments -> user+, moderator, admin
    """

    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        comments = Comment.query.filter_by(post_id=post.id, is_visible=True).all()
        return CommentSchema(many=True).dump(comments), 200

    @jwt_required()
    def post(self, post_id):
        post = Post.query.get_or_404(post_id)
        try:
            data = CommentSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        new_comment = Comment(
            comentario=data['comentario'],
            post_id=post.id,
            author_id=int(get_jwt_identity())
        )
        db.session.add(new_comment)
        db.session.commit()

        return CommentSchema().dump(new_comment), 201


class CommentDetailAPI(MethodView):
    """
    DELETE /api/comments/<id>  -> author, moderator, admin
    PUT    /api/comments/<id>  -> author only
    """

    @jwt_required()
    def delete(self, id):
        comment = Comment.query.get_or_404(id)
        claims = get_jwt()
        current_user_id = int(get_jwt_identity())

        # permisos: autor, moderator, admin
        if claims['role'] not in ['admin', 'moderator'] and not check_ownership(current_user_id, comment.author_id):
            return {"error": "No autorizado"}, 403

        comment.is_visible = False  # soft delete
        db.session.commit()
        return {"message": "Comentario eliminado"}, 200

    @jwt_required()
    def put(self, id):
        comment = Comment.query.get_or_404(id)
        current_user_id = int(get_jwt_identity())

        # solo el autor puede editar
        if not check_ownership(current_user_id, comment.author_id):
            return {"error": "No autorizado"}, 403

        try:
            data = CommentSchema(partial=True).load(request.json)
            if 'comentario' in data:
                comment.comentario = data['comentario']
            db.session.commit()
            return CommentSchema().dump(comment), 200
        except ValidationError as err:
            return {"errors": err.messages}, 400
