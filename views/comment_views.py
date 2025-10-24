from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    @roles_required("admin", "moderator")  # solo admin/moderator puede borrar cualquier comentario
    def delete(self, id):
        """Eliminar cualquier comentario (admin/moderator)"""
        comment = Comment.query.get_or_404(id)
        comment.is_active = False
        db.session.commit()
        return {"message": "Comment deleted"}, 200

    @jwt_required()
    @ownership_required("id")  # solo el autor puede editar
    def put(self, id):
        """Editar comentario solo si eres propietario"""
        comment = Comment.query.get_or_404(id)
        try:
            data = CommentSchema(partial=True).load(request.json)
            if 'content' in data:
                comment.content = data['content']
            db.session.commit()
            return CommentSchema().dump(comment), 200
        except ValidationError as err:
            return {"errors": err.messages}, 400
