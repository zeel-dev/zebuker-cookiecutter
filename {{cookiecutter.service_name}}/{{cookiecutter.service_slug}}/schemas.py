"""Schemas linked to the database models"""
from marshmallow import fields, pre_load
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import ModelSchema


class BaseSchema(ModelSchema):
    """Enables strict validation on Schema"""

    def __init__(self, strict=True, **kwargs):
        super(BaseSchema, self).__init__(strict=strict, **kwargs)