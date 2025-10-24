from app import db
from models import Comment  

class CommentRepository:
    @staticmethod
    def get_all_by_post(post_id):
        return Comment.query.filter_by(post_id=post_id, is_active=True).order_by(Comment.created_at.asc()).all()

    @staticmethod
    def get_by_id(comment_id):
        """Returns a comment by ID"""
        return Comment.query.get(comment_id)

    @staticmethod
    def create_comment(post_id, author_id, comment_text):
        """Creates a new comment"""
        new_comment = Comment(
            post_id=post_id,          
            author_id=author_id,       
            content=comment_text,      
            is_active=True
        )
        db.session.add(new_comment)
        db.session.commit()
        return new_comment

    @staticmethod
    def update_comment(comment, comment_text=None, is_active=None):
        """Updates comment text or visibility"""
        if comment_text is not None:
            comment.content = comment_text   
        if is_active is not None:
            comment.is_active = is_active
        db.session.commit()
        return comment

    @staticmethod
    def delete_comment(comment):
        """Logical delete of the comment"""
        comment.is_active = False
        db.session.commit()
        return comment