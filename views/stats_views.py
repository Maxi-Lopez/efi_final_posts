from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from flask import jsonify

from models import User, Post, Comment, Category
from app import db

class StatsAPI(MethodView):
    @jwt_required()   
    def get(self):
        """
        Devuelve estadísticas globales:
        - cantidad de usuarios
        - cantidad de posts
        - cantidad de comentarios
        - cantidad de categorías
        - top 5 categorías con más posts
        """
        claims = get_jwt()
        role = claims.get("role", "")
        if role != "admin":
            return jsonify({"error": "Not authorized"}), 403

        total_users = db.session.query(User).count()
        total_posts = db.session.query(Post).count()
        total_comments = db.session.query(Comment).count()
        total_categories = db.session.query(Category).count()

        top_categories = (
            db.session.query(Category.name, db.func.count(Post.id).label("total_posts"))
            .join(Post, Post.category_id == Category.id)
            .group_by(Category.name)
            .order_by(db.desc("total_posts"))
            .limit(5)
            .all()
        )

        top_categories_list = [
            {"category": name, "total_posts": total} for name, total in top_categories
        ]

        stats = {
            "total_users": total_users,
            "total_posts": total_posts,
            "total_comments": total_comments,
            "total_categories": total_categories,
            "top_categories": top_categories_list
        }

        return jsonify(stats), 200
