from marshmallow import Schema, fields

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    is_active = fields.Bool(required=False)

    posts = fields.List(
        fields.Nested("PostSchema", exclude=("category",)),
        dump_only=True
    )
