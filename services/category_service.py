from repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def get_all_categories(self, include_inactive=False):
        """Devuelve todas las categorías, opcionalmente incluyendo las inactivas."""
        return self.repo.get_all(include_inactive)

    def get_category_by_id(self, category_id):
        """Devuelve una categoría por su ID."""
        category = self.repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")
        return category

    def get_category_by_name(self, name):
        """Devuelve una categoría por su nombre."""
        return self.repo.get_by_name(name)

    def create_category(self, name):
        """Crea una nueva categoría si no existe otra con el mismo nombre."""
        if self.repo.get_by_name(name):
            raise ValueError("Category with this name already exists")
        return self.repo.create_category(name)

    def update_category(self, category_id, new_name):
        """Actualiza el nombre de una categoría existente."""
        category = self.get_category_by_id(category_id)
        return self.repo.update_category(category, new_name)

    def delete_category(self, category_id):
        """Marca una categoría como inactiva."""
        category = self.get_category_by_id(category_id)
        return self.repo.delete_category(category)
