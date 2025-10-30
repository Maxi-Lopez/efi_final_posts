from models import User, UserCredentials
from app import db

class UserRepository:
    @staticmethod
    def get_all():
        """Devuelve todos los usuarios (incluyendo inactivos)."""
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def get_by_id(user_id):
        """Busca un usuario por ID."""
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        """Busca un usuario por email."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(name, email, password_hash, role="user"):
        """Crea un usuario y sus credenciales en un solo paso."""
        user = User(name=name, email=email, is_active=True)
        db.session.add(user)
        db.session.flush()  # Necesario para obtener el ID

        credentials = UserCredentials(
            user_id=user.id,
            password_hash=password_hash,
            role=role
        )
        db.session.add(credentials)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user, name=None, email=None):
        """Actualiza nombre y email de un usuario."""
        if name:
            user.name = name
        if email:
            user.email = email
        db.session.commit()
        return user

    @staticmethod
    def change_role(user_credentials, new_role):
        """Cambia el rol de las credenciales de un usuario."""
        user_credentials.role = new_role
        db.session.commit()
        return user_credentials

    @staticmethod
    def delete_user(user):
        """Desactiva un usuario y elimina sus credenciales."""
        if hasattr(user, "credential") and user.credential:
            db.session.delete(user.credential)
        user.is_active = False
        db.session.commit()
        return True
