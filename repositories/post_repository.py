from app import db
from models import Post, Category
from datetime import datetime

class PostRepository:
    @staticmethod
    def get_all(include_inactive=False):
        """Devuelve todos los posts, opcionalmente incluyendo inactivos."""
        query = Post.query.order_by(Post.created_at.desc())
        if not include_inactive:
            query = query.filter_by(is_active=True)
        return query.all()

    @staticmethod
    def get_by_id(post_id):
        """Busca un post por ID."""
        return Post.query.get(post_id)

    @staticmethod
    def create_post(title, content, author_id, category_id):
        """Crea un nuevo post."""
        new_post = Post(
            title=title,
            content=content,
            author_id=author_id,
            category_id=category_id,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @staticmethod
    def update_post(post, title=None, content=None, category_id=None):
        """Actualiza un post existente."""
        if title:
            post.title = title
        if content:
            post.content = content
        if category_id:
            post.category_id = category_id
        post.updated_at = datetime.utcnow()
        db.session.commit()
        return post

    @staticmethod
    def delete_post(post):
        """Marca un post como inactivo."""
        post.is_active = False
        post.updated_at = datetime.utcnow()
        db.session.commit()
        return post

    @staticmethod
    def toggle_publish(post, publish_status: bool):
        """Publica o despublica un post."""
        post.is_active = publish_status
        post.updated_at = datetime.utcnow()
        db.session.commit()
        return post

    @staticmethod
    def get_posts_by_category(category_id):
        """Devuelve posts activos de una categoría."""
        return (
            Post.query.filter_by(category_id=category_id, is_active=True)
            .order_by(Post.created_at.desc())
            .all()
        )

    @staticmethod
    def get_or_create_category(name):
        """Obtiene o crea una categoría."""
        category = Category.query.filter_by(name=name).first()
        if not category:
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
        return category
