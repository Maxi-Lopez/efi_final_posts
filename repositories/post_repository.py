from app import db
from models import Post, Category  

class PostRepository:
    @staticmethod
    def get_all(include_inactive=False):
        """Returns all posts, active ones or all if include_inactive=True"""
        if include_inactive:
            return Post.query.order_by(Post.created_at.desc()).all()
        return Post.query.filter_by(is_active=True, is_active=True).order_by(Post.created_at.desc()).all()

    @staticmethod
    def get_by_id(post_id):
        """Returns a post by ID"""
        return Post.query.get(post_id)

    @staticmethod
    def create_post(title, content, author_id, category_id):
        """Creates a new post"""
        new_post = Post(
            title=title,              
            content=content,           
            author_id=author_id,       
            category_id=category_id,   
            is_active=True
        )
        db.session.add(new_post)
        db.session.flush()
        return new_post

    @staticmethod
    def update_post(post, title=None, content=None, category_id=None):
        """Updates an existing post"""
        if title:
            post.title = title        
        if content:
            post.content = content     
        if category_id:
            post.category_id = category_id  
        db.session.commit()
        return post

    @staticmethod
    def delete_post(post):
        """Soft delete: deactivates the post"""
        post.is_active = False
        db.session.commit()
        return post

    @staticmethod
    def toggle_publish(post, publish_status: bool):
        """Publishes or unpublishes a post"""
        post.is_active = publish_status
        db.session.commit()
        return post

    @staticmethod
    def get_posts_by_category(category_id):
        """Returns active posts by category"""
        return Post.query.filter_by(
            category_id=category_id,   
            is_active=True,
            is_active=True
        ).order_by(Post.created_at.desc()).all()