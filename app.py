from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cualquiercosa'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://BD2021:BD2021itec@143.198.156.171:3306/post_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "supersecretjwtkey"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1800

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

from models import User, UserCredentials, Post, Comment, Category
from views.post_views import PostAPI, PostDetailAPI
from views.comment_views import CommentAPI, CommentDetailAPI
from views.category_views import CategoryAPI, CategoryDetailAPI
from views.user_views import UserAPI, UserDetailAPI
from views.user_views import UserRegisterAPI, AuthLoginAPI, UserAPI, UserDetailAPI
from views.stats_views import StatsAPI

# Users
app.add_url_rule('/api/register', view_func=UserRegisterAPI.as_view('register'))
app.add_url_rule('/api/login', view_func=AuthLoginAPI.as_view('login'))
app.add_url_rule('/api/users', view_func=UserAPI.as_view('users'))
app.add_url_rule('/api/users/<int:id>', view_func=UserDetailAPI.as_view('user_detail'))

# Posts
app.add_url_rule("/api/posts", view_func=PostAPI.as_view("posts_api"))
app.add_url_rule("/api/posts/<int:id>", view_func=PostDetailAPI.as_view("post_detail_api"))

# Comments
app.add_url_rule("/api/posts/<int:post_id>/comments", view_func=CommentAPI.as_view("comments_api"))
app.add_url_rule("/api/comments/<int:id>", view_func=CommentDetailAPI.as_view("comment_detail_api"), methods=["GET", "PUT", "DELETE"])

# Categories
app.add_url_rule("/api/categories", view_func=CategoryAPI.as_view("categories_api"))
app.add_url_rule("/api/categories/<int:id>", view_func=CategoryDetailAPI.as_view("category_detail_api"))

# Estadisticas
app.add_url_rule("/api/stats", view_func=StatsAPI.as_view("stats_api"), methods=["GET"])