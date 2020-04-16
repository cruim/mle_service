from marshmallow import Schema, fields, validate, ValidationError
from flask import request, abort

class CreateNoteInputSchema(Schema):
    pclass = fields.Integer(required=True, validate=validate.Range(min=1, max=3))
    name = fields.Str(required=True, validate=validate.Length(max=100))
    sex = fields.Str(required=True, validate=validate.OneOf(["male", "female"]))
    sibsp = fields.Int(required=True)
    parch = fields.Int(required=True)
    embarked = fields.Str(required=True, validate=validate.ContainsOnly(['S', 'C', 'Q']))
    fare = fields.Int(required=True, validate=validate.Range(min=1, max=200))
    age = fields.Int(required=True, validate=validate.Range(min=1, max=100))


schema = CreateNoteInputSchema()


def validate_json(func):
    def wrapper(*args):
        try:
            schema.load(request.get_json())
        except ValidationError as err:
            abort(400, err)
        return func()
    return wrapper
