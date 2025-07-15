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

@app.route('/posts')
def posts():
    categorias = Categoria.query.filter_by(is_active=True).order_by(Categoria.nombre).all()
    return render_template('posts.html', categorias=categorias)


@app.route('/eliminar_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def eliminar_post(post_id):
    post = Contenido.query.get(post_id)
    
    if not post:
        flash('No se encontró el post', 'error')
        return redirect(url_for('posts'))

    categoria = post.categoria

    if request.method == 'POST':
        post.is_active = False
        
        otros_posts_activos = Contenido.query.filter_by(categoria_id=categoria.id, is_active=True).count()

        if otros_posts_activos > 0:
            otros_posts = Contenido.query.filter_by(categoria_id=categoria.id, is_active=True).all()
            for otro_post in otros_posts:
                if otro_post.id != post.id:
                    otro_post.is_active = False   
        else:
             categoria.is_active = False

        db.session.commit()
        flash('Post desactivado exitosamente. Categoría desactivada si es el último post.', 'success')
        return redirect(url_for('posts_por_categoria', categoria_id=categoria.id))
    
    return render_template('eliminar_post.html', post=post)



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


@app.context_processor
def inject_categorias():
    categorias = Categoria.query.filter_by(is_active=True).order_by(Categoria.nombre).all()
    return dict(categorias_disponibles=categorias)


@app.route('/categoria/<int:categoria_id>')
def posts_por_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    posts = Contenido.query.filter_by(categoria_id=categoria.id, is_active=True).order_by(Contenido.fecha.desc()).all()
    return render_template('categoria.html', categoria=categoria, posts=posts)


# Otras rutas que necesito implementar:
# - crear contenido (listo ya fue creado el 09 de Julio)
# - editar_contenido (listo)
# - eliminar_contenido
# - ver_contenido (con comentarios) (listo ya fue creado el 10 de Julio)
# - crear_comentario (listo)
# - gestionar_categorias (listo)
