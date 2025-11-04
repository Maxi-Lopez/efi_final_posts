# README.md

# Proyecto API REST con Flask

Este proyecto es una **API REST** construida con **Flask**, utilizando **SQLAlchemy**, **Marshmallow** y **JWT** para autenticación y autorización basada en roles (RBAC). Permite gestionar usuarios, posts, categorías y comentarios, con control de permisos para distintos roles: `user`, `moderator` y `admin`.

Se utiliza **MethodView** para definir los endpoints de manera modular y clara.

---

## Características

- CRUD de **usuarios**, con registro y login.
- CRUD de **posts** y **categorías**.
- CRUD de **comentarios** asociados a posts.
- Autenticación JWT y manejo de tokens.
- Control de acceso basado en roles ("admin", "moderator" y "user").
- **Soft delete** en posts, comentarios y categorías.
- Estructura modular: `models`, `schemas`, `repositories`, `services`, `views`, `decorators`.
- Validación de datos con **Marshmallow**.
- Seguridad en contraseñas con **passlib** (`bcrypt`).

---

## Estructura del proyecto


```
├── app.py
├── decorators/decorators.py
├── models/
│   ├── category_model.py
│   ├── comment_model.py
│   ├── post_model.py
│   └── user_model.py
├── repositories/
│   ├── category_repository.py
│   ├── comment_repository.py
│   ├── post_repository.py
│   └── user_repository.py
├── schemas/
│   ├── category_schema.py
│   ├── comment_schema.py
│   ├── post_schema.py
│   └── user_schema.py
├── services/
│   ├── category_service.py
│   ├── comment_service.py
│   ├── post_service.py
│   └── user_service.py
└── views/
    ├── category_views.py
    ├── comment_views.py
    ├── post_views.py
    └── user_views.py


---

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/Maxi-Lopez/EFI_LOPEZ_LEJTNEKER.git
cd EFI_LOPEZ_LEJTNEKER
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

4. Ejecutar aplicacion.

```bash
uv run flask run
```

uv run flask run

---

## Uso

5. Inicializar la base de datos y migraciones (si se usa Flask-Migrate):

```bash
flask db init
flask db migrate
flask db upgrade
```

6. Ejecutar la aplicación:

```bash
uv run flask
# o
flask --app app run
```

7. Endpoints principales

*   Usuarios:

    *   POST /api/register → Registro de usuario

    *   POST /api/login → Login

    *   GET /api/users → Listar usuarios

    *   GET /api/users/<id> → Ver usuario

    *   PUT /api/users/<id> → Actualizar usuario

    *   DELETE /api/users/<id> → Eliminar usuario (soft delete)

*   Posts:

    *   GET /api/posts → Listar posts

    *   POST /api/posts → Crear post (requiere JWT)

    *   GET /api/posts/<id> → Ver post

    *   PUT /api/posts/<id> → Editar post (requiere JWT y ownership)

    *   DELETE /api/posts/<id> → Eliminar post (soft delete, requiere JWT y ownership)

    *   Comentarios:

    *   GET /api/posts/<post_id>/comments → Listar comentarios

    *   POST /api/posts/<post_id>/comments → Crear comentario (requiere JWT)

    *   PUT /api/comments/<id> → Editar comentario (requiere JWT y ownership)

    *   DELETE /api/comments/<id> → Eliminar comentario (soft delete, requiere JWT y ownership)

*   Categorías:

    *   GET /api/categories → Listar categorías

    *   POST /api/categories → Crear categoría (requiere JWT)

    *   GET /api/categories/<id> → Ver categoría

    *   PUT /api/categories/<id> → Editar categoría (requiere JWT)

    *   DELETE /api/categories/<id> → Eliminar categoría (soft delete, requiere JWT)

*   Estadísticas:

    *   GET /api/stats → Obtener estadísticas generales de posts y comentarios

---

## Tecnologías utilizadas

- Python 3.x

- Flask

- Flask-JWT-Extended

- Flask-Migrate

- Flask-CORS

- SQLAlchemy

- Marshmallow

- passlib (bcrypt)

- MySQL / MariaDB

---

## Autores

**Maximiliano Lopez y Agustin Lejtneker** 
Idea original basada en la estructura de Matías Javier Lucero.

