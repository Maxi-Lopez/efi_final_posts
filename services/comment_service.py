from repositories.comment_repository import CommentRepository

class CommentService:
    def __init__(self):
        self.repo = CommentRepository()

    def get_comments_for_post(self, post_id):
        """Obtiene todos los comentarios activos de un post."""
        return self.repo.get_all_by_post(post_id)

    def get_comment_by_id(self, comment_id):
        """Obtiene un comentario por su ID."""
        comment = self.repo.get_by_id(comment_id)
        if not comment:
            raise ValueError("Comment not found")
        return comment

    def create_comment(self, post_id, author_id, comment_text):
        """Crea un nuevo comentario asociado a un post."""
        return self.repo.create_comment(post_id, author_id, comment_text)

    def update_comment(self, comment_id, comment_text=None, is_active=None):
        """Actualiza el texto o estado de un comentario."""
        comment = self.get_comment_by_id(comment_id)
        return self.repo.update_comment(comment, comment_text, is_active)

    def delete_comment(self, comment_id):
        """Elimina (lógicamente) un comentario."""
        comment = self.get_comment_by_id(comment_id)
        return self.repo.delete_comment(comment)
