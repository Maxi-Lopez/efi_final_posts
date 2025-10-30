from passlib.hash import bcrypt
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def get_all_users(self, include_inactive=False):
        """Obtiene todos los usuarios (puede incluir inactivos)."""
        users = self.repo.get_all()
        if not include_inactive:
            users = [u for u in users if u.is_active]
        return users

    def get_user_by_id(self, user_id):
        """Obtiene un usuario por ID."""
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    def create_user(self, name, email, password, role="user"):
        """Crea un nuevo usuario con credenciales."""
        if self.repo.get_by_email(email):
            raise ValueError("Email already in use")

        new_user = self.repo.create_user(name, email)

        credentials = new_user.credential or self.repo.create_credentials(
            user_id=new_user.id,
            password_hash=bcrypt.hash(password),
            role=role
        )
        return new_user

    def update_user(self, user_id, name=None, email=None):
        """Actualiza un usuario existente."""
        user = self.get_user_by_id(user_id)
        updated_user = self.repo.update_user(user, name, email)
        return updated_user

    def change_role(self, user_id, new_role):
        """Cambia el rol de un usuario."""
        user = self.get_user_by_id(user_id)
        if not hasattr(user, "credential") or not user.credential:
            raise ValueError("User has no credentials")
        if new_role not in ["user", "moderator", "admin"]:
            raise ValueError("Invalid role")
        self.repo.change_role(user.credential, new_role)
        return user

    def delete_user(self, user_id):
        """Desactiva un usuario y sus credenciales."""
        user = self.get_user_by_id(user_id)
        self.repo.delete_user(user)
        return True
