from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app import db
from models import Comment
from schemas import CommentSchema
from decorators.decorators import roles_required, ownership_required

class CommentAPI(MethodView):
    def get(self, post_id):
        """Cualquiera puede ver los comentarios"""
        comments = Comment.query.filter_by(post_id=post_id, is_active=True).all()
        return CommentSchema(many=True).dump(comments), 200

    @jwt_required()
    def post(self, post_id):
        """Solo usuarios logueados pueden comentar"""
        user_id = int(get_jwt_identity())
        data = request.get_json()
        new_comment = Comment(
            post_id=post_id,
            author_id=user_id,
            content=data["content"],
            is_active=True
        )
        db.session.add(new_comment)
        db.session.commit()
        return CommentSchema().dump(new_comment), 201

class CommentDetailAPI(MethodView):

    @jwt_required()
    def put(self, id):
        """Editar comentario solo si eres propietario o admin/moderator"""
        comment = Comment.query.get_or_404(id)
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        role = claims.get("role", "")

        if role not in ["admin", "moderator"] and comment.author_id != current_user_id:
            return {"error": "Not authorized"}, 403

        data = request.get_json()
        if 'content' in data:
            comment.content = data['content']
        db.session.commit()
        return CommentSchema().dump(comment), 200

    @jwt_required()
    def delete(self, id):
        """Eliminar comentario si eres admin/moderator o el autor"""
        comment = Comment.query.get_or_404(id)
        user_id = int(get_jwt_identity())
        claims = get_jwt()
        role = claims.get("role", "")

        # Check ownership o rol
        if role in ["admin", "moderator"] or comment.author_id == user_id:
            comment.is_active = False
            db.session.commit()
            return {"message": "Comment deleted"}, 200
        else:
            return {"error": "Not authorized"}, 403