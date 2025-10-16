# services/comment_service.py

from repositories.comment_repository import CommentRepository


class CommentService:
    def __init__(self):
        self.repo = CommentRepository()

    def get_comments_for_post(self, post_id):
        """Obtiene todos los comentarios visibles de un post"""
        return self.repo.get_all_by_post(post_id)

    def get_comment_by_id(self, comment_id):
        """Obtiene un comentario por ID"""
        return self.repo.get_by_id(comment_id)

    def create_comment(self, post_id, author_id, comment_text):
        """Crea un comentario en un post"""
        return self.repo.create_comment(post_id, author_id, comment_text)

    def update_comment(self, comment_id, comment_text=None, is_visible=None):
        """Actualiza un comentario"""
        comment = self.get_comment_by_id(comment_id)
        return self.repo.update_comment(comment, comment_text, is_visible)

    def delete_comment(self, comment_id):
        """Elimina (soft delete) un comentario"""
        comment = self.get_comment_by_id(comment_id)
        return self.repo.delete_comment(comment)
