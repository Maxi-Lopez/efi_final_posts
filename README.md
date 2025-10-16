# README.md

# Proyecto API REST con Flask

Este proyecto es una **API REST** construida con **Flask**, usando **SQLAlchemy**, **Marshmallow**, y **JWT** para autenticación y autorización basada en roles (RBAC). Permite gestionar usuarios, posts, categorías y comentarios, con control de permisos para distintos roles: `user`, `moderator`, `admin`.

---

## Características

- CRUD de **usuarios**, con registro y login.
- CRUD de **posts** y **categorías**.
- CRUD de **comentarios** asociados a posts.
- Autenticación JWT.
- Control de acceso basado en roles (RBAC).
- Soft delete en posts, comentarios y categorías.
- Estructura modular: `models`, `schemas`, `repositories`, `services`, `views`.
- Validación de datos con **Marshmallow**.
- Seguridad en passwords con **passlib** (`bcrypt`).

---

## Estructura del proyecto

```
.
├── app.py
├── decorators.py
├── utils.py
├── requirements.txt
├── models/
│   ├── __init__.py
│   ├── user_model.py
│   ├── post_model.py
│   ├── comment_model.py
│   └── category_model.py
├── schemas/
│   ├── __init__.py
│   ├── user_schema.py
│   ├── post_schema.py
│   ├── comment_schema.py
│   └── category_schema.py
├── repositories/
│   ├── user_repository.py
│   ├── post_repository.py
│   └── comment_repository.py
├── services/
│   ├── user_service.py
│   ├── post_service.py
│   └── comment_service.py
└── views/
    ├── auth_views.py
    ├── user_views.py
    ├── post_views.py
    ├── comment_views.py
    └── category_views.py
```

---

## Instalación

1. Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_REPOSITORIO>
```

2. Crear y activar entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno (por ejemplo, secret key para JWT).

---

## Uso

1. Inicializar la base de datos y migraciones (si se usa Flask-Migrate):

```bash
flask db init
flask db migrate
flask db upgrade
```

2. Ejecutar la aplicación:

```bash
uv run flask
# o
flask --app app run
```

3. Acceder a las rutas de la API según los endpoints definidos en los views:

- `/api/register` → Registro de usuario
- `/api/login` → Login
- `/api/users` → Gestión de usuarios
- `/api/posts` → Gestión de posts
- `/api/categories` → Gestión de categorías
- `/api/posts/<id>/comments` → Gestión de comentarios

---

## Tecnologías

- Python 3.x
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- Marshmallow
- passlib (bcrypt)
- PostgreSQL / MySQL / SQLite (según configuración)

---

## Autor

**Maxi Lopez**  
Idea original basada en la estructura de Matías Javier Lucero.

