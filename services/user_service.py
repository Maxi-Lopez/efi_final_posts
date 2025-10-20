from app import db
from models import User, UserCredentials
from passlib.hash import bcrypt

class UserService:
    def __init__(self):
        pass

    def get_all_users(self):
        return User.query.all()

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

    def create_user(self, name, email, password, role="user"):
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already in use")

        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.flush()

        password_hash = bcrypt.hash(password)
        credentials = UserCredentials(
            user_id=new_user.id,
            password_hash=password_hash,
            role=role
        )
        db.session.add(credentials)
        db.session.commit()

        return new_user

    def update_user(self, user_id, name=None, email=None):
        user = User.query.get_or_404(user_id)
        if name:
            user.name = name
        if email:
            user.email = email
        db.session.commit()
        return user

    def change_role(self, user_id, new_role):
        user = User.query.get_or_404(user_id)
        if not hasattr(user, "credential") or not user.credential:
            raise ValueError("User has no credentials")
        if new_role not in ["user", "moderator", "admin"]:
            raise ValueError("Invalid role")
        user.credential.role = new_role
        db.session.commit()
        return user

    def delete_user(self, user_id):
        user = User.query.get_or_404(user_id)
        if hasattr(user, "credential") and user.credential:
            db.session.delete(user.credential)
        user.is_active = False
        db.session.commit()
        return True