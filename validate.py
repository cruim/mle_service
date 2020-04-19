from marshmallow import Schema, fields, validate, ValidationError
from flask import request, abort


class NestedSchema(Schema):
    pclass = fields.Integer(required=True, validate=validate.Range(min=1, max=3))
    name = fields.String(required=True, validate=validate.Length(max=100))
    sex = fields.String(required=True, validate=validate.OneOf(["male", "female"]))
    sibsp = fields.Integer(required=True)
    parch = fields.Integer(required=True)
    embarked = fields.String(required=True, validate=validate.ContainsOnly(['S', 'C', 'Q']))
    fare = fields.Integer(required=True, validate=validate.Range(min=1, max=200))
    age = fields.Int(required=True, validate=validate.Range(min=1, max=100))


class ModelSchema(Schema):
    models = fields.List(fields.String(), required=True, validate=validate.Length(min=1))
    data = fields.Nested(NestedSchema)


schema = ModelSchema()


def validate_json(func):
    def wrapper(*args):
        try:
            schema.load(request.get_json())
        except ValidationError as err:
            abort(400, err)
        return func()
    return wrapper
