from datetime import datetime
from repositories.post_repository import PostRepository

class PostService:
    def __init__(self):
        self.repo = PostRepository()

    def get_all_posts(self, include_inactive=False):
        """Obtiene todos los posts (puede incluir inactivos)."""
        return self.repo.get_all(include_inactive)

    def get_post_by_id(self, post_id):
        """Obtiene un post por su ID."""
        post = self.repo.get_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        return post

    def create_post(self, title, content, author_id, category_name):
        """Crea un post y su categoría si no existe."""
        category = self.repo.get_or_create_category(category_name)
        new_post = self.repo.create_post(
            title=title,
            content=content,
            author_id=author_id,
            category_id=category.id
        )
        return new_post

    def update_post(self, post_id, title=None, content=None, category_name=None):
        """Actualiza un post existente."""
        post = self.get_post_by_id(post_id)
        category_id = None
        if category_name:
            category = self.repo.get_or_create_category(category_name)
            category_id = category.id
        updated_post = self.repo.update_post(
            post, title=title, content=content, category_id=category_id
        )
        return updated_post

    def delete_post(self, post_id):
        """Desactiva un post."""
        post = self.get_post_by_id(post_id)
        return self.repo.delete_post(post)

    def toggle_publish(self, post_id, publish_status: bool):
        """Publica o despublica un post."""
        post = self.get_post_by_id(post_id)
        return self.repo.toggle_publish(post, publish_status)

    def get_posts_by_category(self, category_id):
        """Obtiene posts activos de una categoría."""
        return self.repo.get_posts_by_category(category_id)
