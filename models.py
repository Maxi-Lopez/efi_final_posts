from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    contenidos = db.relationship('Contenido', backref='autor', lazy=True, cascade='all, delete-orphan')
    comentarios = db.relationship('Comentario', backref='autor', lazy=True, cascade='all, delete-orphan')

    def __str__(self):
        return f"{self.username}"

class Contenido(db.Model):
    __tablename__ = 'contenido'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    comentarios = db.relationship('Comentario', backref='contenido_rel', lazy=True, cascade='all, delete-orphan')
    categoria = db.relationship('Categoria', backref='contenidos')

    def __str__(self):
        return f"{self.titulo} - {self.fecha.strftime('%d/%m/%Y')}"

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contenido_id = db.Column(db.Integer, db.ForeignKey('contenido.id'), nullable=False)

    def __str__(self):
        return f"Comentario de {self.autor.username} en post {self.contenido_rel.titulo}"

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    def __str__(self):
        return self.nombre
