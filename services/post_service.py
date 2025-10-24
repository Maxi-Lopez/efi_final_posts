from app import db
from models import Post, Category
from datetime import datetime

class PostService:
    def __init__(self):
        pass

    def get_all_posts(self, include_inactive=False):
        if include_inactive:
            return Post.query.order_by(Post.created_at.desc()).all()
        return Post.query.filter_by(is_active=True, is_active=True).order_by(Post.created_at.desc()).all()

    def get_post_by_id(self, post_id):
        return Post.query.get_or_404(post_id)

    def create_post(self, title, content, author_id, category_name):
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.flush()

        new_post = Post(
            title=title,
            content=content,
            author_id=author_id,
            category_id=category.id,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post

    def update_post(self, post_id, title=None, content=None, category_name=None):
        post = self.get_post_by_id(post_id)
        if title:
            post.title = title
        if content:
            post.content = content
        if category_name:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.flush()
            post.category_id = category.id
        post.updated_at = datetime.utcnow()
        db.session.commit()
        return post

    def delete_post(self, post_id):
        post = self.get_post_by_id(post_id)
        post.is_active = False
        db.session.commit()
        return post

    def toggle_publish(self, post_id, publish_status: bool):
        post = self.get_post_by_id(post_id)
        post.is_active = publish_status
        post.updated_at = datetime.utcnow()
        db.session.commit()
        return post

    def get_posts_by_category(self, category_id):
        return Post.query.filter_by(
            category_id=category_id, 
            is_active=True, 
            is_active=True
        ).order_by(Post.created_at.desc()).all()