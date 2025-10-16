# repositories/post_repository.py

from app import db
from models import Contenido, Categoria


class PostRepository:
    @staticmethod
    def get_all(include_inactive=False):
        """Devuelve todos los posts, activos o todos si include_inactive=True"""
        if include_inactive:
            return Contenido.query.order_by(Contenido.fecha.desc()).all()
        return Contenido.query.filter_by(is_active=True, is_published=True).order_by(Contenido.fecha.desc()).all()

    @staticmethod
    def get_by_id(post_id):
        """Devuelve un post por ID"""
        return Contenido.query.get(post_id)

    @staticmethod
    def create_post(title, content, author_id, category_id):
        """Crea un post nuevo"""
        new_post = Contenido(
            titulo=title,
            contenido=content,
            autor_id=author_id,
            categoria_id=category_id,
            is_published=True
        )
        db.session.add(new_post)
        db.session.flush()
        return new_post

    @staticmethod
    def update_post(post, title=None, content=None, category_id=None):
        """Actualiza un post existente"""
        if title:
            post.titulo = title
        if content:
            post.contenido = content
        if category_id:
            post.categoria_id = category_id
        db.session.commit()
        return post

    @staticmethod
    def delete_post(post):
        """Soft delete: desactiva el post"""
        post.is_active = False
        db.session.commit()
        return post

    @staticmethod
    def toggle_publish(post, publish_status: bool):
        """Publica o despublica un post"""
        post.is_published = publish_status
        db.session.commit()
        return post

    @staticmethod
    def get_posts_by_category(category_id):
        """Devuelve posts activos por categoría"""
        return Contenido.query.filter_by(
            categoria_id=category_id,
            is_active=True,
            is_published=True
        ).order_by(Contenido.fecha.desc()).all()
