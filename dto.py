from marshmallow import fields, Schema

class UserDto(Schema):
    id = fields.Int()
    username = fields.String()
    email = fields.String()
    password = fields.String()
    role = fields.String()