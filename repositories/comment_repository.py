from app import db
from models import Comentario


class CommentRepository:
    @staticmethod
    def get_all_by_post(post_id):
        """Devuelve todos los comentarios visibles de un post"""
        return Comentario.query.filter_by(contenido_id=post_id, is_visible=True).order_by(Comentario.fecha_creacion.asc()).all()

    @staticmethod
    def get_by_id(comment_id):
        """Devuelve un comentario por ID"""
        return Comentario.query.get(comment_id)

    @staticmethod
    def create_comment(post_id, author_id, comment_text):
        """Crea un nuevo comentario"""
        new_comment = Comentario(
            contenido_id=post_id,
            autor_id=author_id,
            comentario=comment_text,
            is_visible=True
        )
        db.session.add(new_comment)
        db.session.commit()
        return new_comment

    @staticmethod
    def update_comment(comment, comment_text=None, is_visible=None):
        """Actualiza el texto o visibilidad de un comentario"""
        if comment_text is not None:
            comment.comentario = comment_text
        if is_visible is not None:
            comment.is_visible = is_visible
        db.session.commit()
        return comment

    @staticmethod
    def delete_comment(comment):
        """Borrado logico del comentario"""
        comment.is_visible = False
        db.session.commit()
        return comment
