from app import db
from models import Contenido, Categoria
from datetime import datetime


class PostService:
    def __init__(self):
        pass

    def get_all_posts(self, include_inactive=False):
        """Devuelve todos los posts publicados (o todos si include_inactive=True)"""
        if include_inactive:
            return Contenido.query.order_by(Contenido.fecha.desc()).all()
        return Contenido.query.filter_by(is_active=True, is_published=True).order_by(Contenido.fecha.desc()).all()

    def get_post_by_id(self, post_id):
        """Devuelve un post por ID"""
        return Contenido.query.get_or_404(post_id)

    def create_post(self, title, content, author_id, category_name):
        """Crea un nuevo post y asigna categoría"""
        category = Categoria.query.filter_by(nombre=category_name).first()
        if not category:
            category = Categoria(nombre=category_name)
            db.session.add(category)
            db.session.flush()

        new_post = Contenido(
            titulo=title,
            contenido=content,
            autor_id=author_id,
            categoria_id=category.id,
            is_published=True,
            fecha=datetime.utcnow()
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post

    def update_post(self, post_id, title=None, content=None, category_name=None):
        """Actualiza un post existente"""
        post = self.get_post_by_id(post_id)
        if title:
            post.titulo = title
        if content:
            post.contenido = content
        if category_name:
            category = Categoria.query.filter_by(nombre=category_name).first()
            if not category:
                category = Categoria(nombre=category_name)
                db.session.add(category)
                db.session.flush()
            post.categoria_id = category.id
        post.updated_at = datetime.utcnow()
        db.session.commit()
        return post

    def delete_post(self, post_id):
        """Soft delete: desactiva el post"""
        post = self.get_post_by_id(post_id)
        post.is_active = False
        db.session.commit()
        return post

    def toggle_publish(self, post_id, publish_status: bool):
        """Publica o despublica un post"""
        post = self.get_post_by_id(post_id)
        post.is_published = publish_status
        post.updated_at = datetime.utcnow()
        db.session.commit()
        return post

    def get_posts_by_category(self, category_id):
        """Devuelve posts activos por categoría"""
        return Contenido.query.filter_by(
            categoria_id=category_id, 
            is_active=True, 
            is_published=True
        ).order_by(Contenido.fecha.desc()).all()
