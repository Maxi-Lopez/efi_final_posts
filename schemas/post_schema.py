from marshmallow import Schema, fields

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_published = fields.Bool(dump_only=True)
    author_id = fields.Int(dump_only=True)
    category_id = fields.Int(allow_none=True)

    author = fields.Nested("UserSchema", only=["id", "name"], dump_only=True)
    category = fields.Nested("CategorySchema", only=["id", "name"], dump_only=True)
    comments = fields.List(
        fields.Nested("CommentSchema", exclude=("post",)),
        dump_only=True
    )