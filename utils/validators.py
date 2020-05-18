from marshmallow import Schema, fields, pprint


class Todo(Schema):
    id = fields.Int(required=False)
    title = fields.Str()
    done = fields.Bool()
