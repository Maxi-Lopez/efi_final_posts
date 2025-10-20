from app import db
from models import Comment  

class CommentRepository:
    @staticmethod
    def get_all_by_post(post_id):
        return Comment.query.filter_by(post_id=post_id, is_visible=True).order_by(Comment.created_at.asc()).all()

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
            is_visible=True
        )
        db.session.add(new_comment)
        db.session.commit()
        return new_comment

    @staticmethod
    def update_comment(comment, comment_text=None, is_visible=None):
        """Updates comment text or visibility"""
        if comment_text is not None:
            comment.content = comment_text   
        if is_visible is not None:
            comment.is_visible = is_visible
        db.session.commit()
        return comment

    @staticmethod
    def delete_comment(comment):
        """Logical delete of the comment"""
        comment.is_visible = False
        db.session.commit()
        return comment