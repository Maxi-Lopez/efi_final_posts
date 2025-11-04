from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    is_active = fields.Bool(required=False)
    created_at = fields.DateTime(dump_only=True)

    posts = fields.List(
        fields.Nested("PostSchema", exclude=("author",)),
        dump_only=True
    )
    comments = fields.List(
        fields.Nested("CommentSchema", exclude=("author",)),
        dump_only=True
    )


class UserDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Email()
    is_active = fields.Bool(required=False)
    created_at = fields.DateTime(dump_only=True)
    role = fields.Str(dump_only=True)  


class RegisterSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(load_only=True)
    
    def validate_role(self, value):
        if value and value != 'user':
            raise ValidationError("Only 'user' role can be assigned during registration")


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

 
