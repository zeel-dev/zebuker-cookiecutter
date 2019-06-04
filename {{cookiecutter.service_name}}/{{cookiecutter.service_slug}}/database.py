"""Database definitions and extensions, including the flask-sqlalchemy instance

TODO - We probably want to alias all sqlalchemy definitions that we will be
using in our models. As it stands, we *can* import Type, relationship and
Column definitions directly from sqlalchemy but there is no real reason to
not import from the flask-sqlalchemy instance.
"""
from random import choices
from datetime import datetime
import string

from {{ cookiecutter.service_slug }} import db
from sqlalchemy import DateTime

# Alias common SQLAlchemy names
Column = db.Column
Model = db.Model


def rand_string_id(length):
    """Return a randomly generated string of Uppercase letters and digits

    Parameters
    ----------
    length : int
        Desired length of the random string
    """
    return ''.join(choices(string.ascii_uppercase + string.digits, k=length))


class CrudMixin(object):
    """Mixin that adds convenience methods for CRUD"""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class TimestampMixin(object):
    """Class to add timestamp fields to tables"""

    inserted = Column(DateTime, default=datetime.utcnow)
    updated = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
