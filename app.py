# app/app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Inicialización
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cualquiercosa'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/efi_1er_semestre"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "supersecretjwtkey"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24h en segundos

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# -------------------------------
# Importar modelos, schemas y views
# -------------------------------
from models import User, UserCredentials, Post, Comment, Category
from views.post_views import PostAPI, PostDetailAPI
from views.comment_views import CommentAPI, CommentDetailAPI
from views.category_views import CategoryAPI, CategoryDetailAPI
from views.user_views import UserAPI, UserDetailAPI
from views.auth_views import UserRegisterAPI, AuthLoginAPI

# -------------------------------
# Registrar rutas como MethodView
# -------------------------------

# Usuarios
app.add_url_rule("/api/users", view_func=UserAPI.as_view("users_api"))
app.add_url_rule("/api/users/<int:id>", view_func=UserDetailAPI.as_view("user_detail_api"))
app.add_url_rule("/api/register", view_func=UserRegisterAPI.as_view("user_register_api"))
app.add_url_rule("/api/login", view_func=AuthLoginAPI.as_view("auth_login_api"))

# Posts
app.add_url_rule("/api/posts", view_func=PostAPI.as_view("posts_api"))
app.add_url_rule("/api/posts/<int:id>", view_func=PostDetailAPI.as_view("post_detail_api"))

# Comentarios
app.add_url_rule("/api/posts/<int:post_id>/comments", view_func=CommentAPI.as_view("comments_api"))
app.add_url_rule("/api/comments/<int:id>", view_func=CommentDetailAPI.as_view("comment_detail_api"))

# Categorías
app.add_url_rule("/api/categories", view_func=CategoryAPI.as_view("categories_api"))
app.add_url_rule("/api/categories/<int:id>", view_func=CategoryDetailAPI.as_view("category_detail_api"))

# -------------------------------
# Endpoint raíz opcional
# -------------------------------
@app.route("/")
def index():
    return {"message": "API REST funcionando 🚀"}

# -------------------------------
# Run server (solo si se ejecuta directamente)
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
