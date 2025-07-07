import requests
from    datetime import date

from flask import Flask, flash, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, 
    login_user, 
    login_required, 
    logout_user, 
    current_user,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)


app = Flask(__name__)

app.secret_key = "cualquiercosa"
app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+pymysql://root:@localhost/efi_1er_semestre")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, Entrada, Comentario, Categoria

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')  
        password = request.form.get('password')
        
        if not username or not password:  
            flash('Por favor ingrese usuario y contraseña', 'error')
            return redirect(url_for('login'))
            
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):  
            login_user(user)
            flash('¡Bienvenido!', 'success')
            next_page = request.args.get('next')   
            return redirect(next_page or url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('auth/login.html')   

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            flash('Todos los campos son obligatorios', 'error')
        elif password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
        elif User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe', 'error')
        elif User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
        else:
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                is_active=True
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registro exitoso. Por favor inicie sesión', 'success')
            return redirect(url_for('login'))
    
    return render_template('auth/register.html')  


@app.route('/posts')
def posts():
    posts = Entrada.query.filter_by(is_active=True).all()
    return render_template('posts.html', posts=posts)



@app.route('/crear_posts')
def crear_posts():
    posts = Entrada.query.filter_by(is_active=True).all()
    return render_template('crear_posts.html', posts=posts)

#Falta hacer el formulario de crear post 
#Falta hacer el formulario de editar post
#Falta hacer el formulario de eliminar post
#Falta hacer el formulario de editar usuario
#Falta hacer el formulario de eliminar usuario
#Falta hacer el formulario de editar entrada
#Falta hacer el formulario de eliminar entrada
#Falta hacer el formulario de editar comentario
#Falta hacer el formulario de eliminar comentario
#Falta hacer el formulario de editar respuesta
#Falta hacer el formulario de eliminar respuesta
#Falta hacer el formulario de editar categoria
#Falta hacer el formulario de eliminar categoria
