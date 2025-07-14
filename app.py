import requests
from datetime import date
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
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/efi_1er_semestre"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, Contenido, Comentario, Categoria

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

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        contenidos = Contenido.query.filter_by(is_active=True).all()
        return render_template('posts.html', contenidos=contenidos)
    return render_template('posts.html')

@app.route('/editar_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    if request.method == 'GET':
        contenido = Contenido.query.get_or_404(post_id)
        return render_template('editar_post.html', contenido=contenido)
    else:
        contenido = Contenido.query.get_or_404(post_id)

        nuevo_categoria = request.form.get('categoria', "").strip()
        nuevo_titulo = request.form.get('titulo', "").strip()
        nuevo_contenido = request.form.get('contenido', "").strip()

        contenido.titulo = nuevo_titulo
        contenido.contenido = nuevo_contenido

        if nuevo_categoria:
            categoria = Categoria.query.filter_by(nombre=nuevo_categoria).first()
            if not categoria:
                categoria = Categoria(nombre=nuevo_categoria)
                db.session.add(categoria)
                db.session.flush()
            contenido.categoria_id = categoria.id

        db.session.commit()

    return redirect(url_for('posts'))

@app.route('/eliminar_post')
@login_required
def eliminar_post():
    contenidos = Contenido.query.filter_by(is_active=True).all()
    return redirect(url_for('eliminar_post'))

@app.route('/crear_posts', methods=['GET', 'POST'])
@login_required
def crear_posts():
    if request.method == 'POST':
        nombre_categoria = request.form.get('categoria', "").strip()
        titulo = request.form.get('titulo', "").strip()
        contenido_texto = request.form.get('contenido', "").strip()
        if not all([nombre_categoria, titulo, contenido_texto]):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('crear_posts'))

        categoria = Categoria.query.filter_by(nombre=nombre_categoria).first()
        if not categoria:
            categoria = Categoria(nombre=nombre_categoria)
            db.session.add(categoria)
            db.session.commit()
         
        nuevo_contenido = Contenido(
            titulo=titulo,
            contenido=contenido_texto,
            autor_id=current_user.id,
            categoria_id=categoria.id
        )
        db.session.add(nuevo_contenido)
        db.session.commit()
        
        flash('Publicación creada exitosamente', 'success')
        return redirect(url_for('posts'))

    return render_template('crear_posts.html')

@app.route('/comentar_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comentar_post(post_id):
    contenido = Contenido.query.get_or_404(post_id)
    if request.method == 'POST':
        comentario_texto = request.form.get('comentario', '').strip()

        if not comentario_texto:
            flash('El comentario no puede estar vacío.', 'error')
            return redirect(url_for('comentar_post', post_id=post_id))

        nuevo_comentario = Comentario(
            comentario=comentario_texto,
            autor_id=current_user.id,
            contenido_id=contenido.id
        )

        db.session.add(nuevo_comentario)
        db.session.commit()
        flash('Comentario creado exitosamente.', 'success')
        return redirect(url_for('posts'))

    return render_template('comentar_post.html', contenido=contenido)

@app.route('/ver_comentarios/<int:post_id>')
def ver_comentarios(post_id):
    contenido = Contenido.query.get_or_404(post_id)
    comentarios = Comentario.query.filter_by(contenido_id=post_id).all()
    
    return render_template('ver_comentarios.html', contenido=contenido, comentarios=comentarios)



# Otras rutas que necesito implementar:
# - crear contenido (listo ya fue creado el 09 de Julio)
# - editar_contenido (listo)
# - eliminar_contenido
# - ver_contenido (con comentarios) (listo ya fue creado el 10 de Julio)
# - crear_comentario
# - gestionar_categorias
