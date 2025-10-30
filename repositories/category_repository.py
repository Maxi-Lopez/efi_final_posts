from app import db
from models import Category

class CategoryRepository:
    @staticmethod
    def get_all(include_inactive=False):
        """Devuelve todas las categorías, opcionalmente incluyendo inactivas."""
        query = Category.query.order_by(Category.name.asc())
        if not include_inactive:
            query = query.filter_by(is_active=True)
        return query.all()

    @staticmethod
    def get_by_id(category_id):
        """Busca una categoría por ID."""
        return Category.query.get(category_id)

    @staticmethod
    def get_by_name(name):
        """Busca una categoría por nombre."""
        return Category.query.filter_by(name=name).first()

    @staticmethod
    def create_category(name):
        """Crea una nueva categoría."""
        category = Category(name=name, is_active=True)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def update_category(category, new_name):
        """Actualiza el nombre de una categoría existente."""
        category.name = new_name
        db.session.commit()
        return category

    @staticmethod
    def delete_category(category):
        """Marca una categoría como inactiva."""
        category.is_active = False
        db.session.commit()
        return category
