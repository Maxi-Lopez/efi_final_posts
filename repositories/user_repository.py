from models import User, UserCredentials
from app import db

class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(name, email):
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.flush() 
        return user

    @staticmethod
    def update_user(user, name=None, email=None):
        if name:
            user.name = name
        if email:
            user.email = email
        db.session.commit()
        return user

    @staticmethod
    def change_role(user_credentials, new_role):
        user_credentials.role = new_role
        db.session.commit()
        return user_credentials

    @staticmethod
    def delete_user(user):
        user.is_active = False
        db.session.commit()
        return True