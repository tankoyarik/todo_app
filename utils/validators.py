from marshmallow import Schema, fields


class Todo(Schema):
    id = fields.Int(required=False)
    title = fields.Str()
    done = fields.Bool()
