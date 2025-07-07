from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    posts = db.relationship('Entrada', backref='autor_user', lazy=True)
    comentarios = db.relationship('Comentario', backref='autor_user', lazy=True)

    def __str__(self):
        return f"{self.username}"

class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=True) 

    is_active = db.Column(db.Boolean, default=True)

    comentarios = db.relationship('Comentario', backref='entrada', lazy=True)
    categoria = db.relationship('Categoria', backref='entradas') 

    def __str__(self):
        return f"{self.titulo} - {self.fecha}"

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrada.id'), nullable=False)

    def __str__(self):
        return f"Comentario de {self.autor_id} en entrada {self.entrada_id}"

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.nombre
