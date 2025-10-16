from marshmallow import Schema, fields

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    comentario = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    is_visible = fields.Bool(dump_only=True)
    author_id = fields.Int(dump_only=True)
    post_id = fields.Int(required=True)

    author = fields.Nested("UserSchema", only=["id", "name"], dump_only=True)
    post_rel = fields.Nested("PostSchema", only=["id", "title"], dump_only=True)
