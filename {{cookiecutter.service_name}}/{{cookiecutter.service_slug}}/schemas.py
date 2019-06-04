"""Schemas linked to the database models"""
import re
from marshmallow import post_dump
from marshmallow_sqlalchemy import ModelSchema


class BaseSchema(ModelSchema):
    """
    Custom base schema class that serializes datetime strings without the
    timezone offset.
    """

    def __init__(self, strict=True, **kwargs):
        super(BaseSchema, self).__init__(strict=strict, **kwargs)

    @post_dump
    def strip_timezone_offset(self, data):
        """Strips timezone offset from ISO8601/RFC3339 strings"""
        for key in data:
            if data[key] and isinstance(data[key], str):
                matches = re.match(
                    r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d{6})?[+-]\d\d:\d\d$',
                    data[key]
                )
                if matches:
                    data[key] = data[key][:-6]

        return data