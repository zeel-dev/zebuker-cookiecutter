"""Helper module for Database and Schema creation/deletion.

In order for create_tables and drop_tables to work properly, all Model classes
must be explicitly imported so that their metadata can be registered with
SQLAlchemy.
"""
from flask_sqlalchemy import sqlalchemy
import sqlalchemy_utils.functions as sqlalchemy_utils

from {{cookiecutter.service_slug}}.database import db
# Explicit model imports. Flake8 F401 warning deliberately ignored here.
from {{cookiecutter.service_slug}}.models.area_boundary import AreaBoundary
from {{cookiecutter.service_slug}}.models.area_data_numeric import AreaDataNumeric
from {{cookiecutter.service_slug}}.models.area_relationship import AreaRelationship
from {{cookiecutter.service_slug}}.models.area import Area
from {{cookiecutter.service_slug}}.models.business_line_type import BusinessLineType
from {{cookiecutter.service_slug}}.models.currency_type import CurrencyType
from {{cookiecutter.service_slug}}.models.price_point import PricePoint
from {{cookiecutter.service_slug}}.models.product import Product
from {{cookiecutter.service_slug}}.models.quantity_type import QuantityType


def create_database(flask_app):
    """Create a Postgres database instance and a postgis extension.

    Probably should not be used outside of the context of flask application
    (needs more testing)
    """
    engine = sqlalchemy.create_engine(
        flask_app.config.get('SQLALCHEMY_DATABASE_URI')
    )

    # Create database
    if not sqlalchemy_utils.database_exists(engine.url):
        sqlalchemy_utils.create_database(engine.url)

    # Create postgis extension
    engine.execute('CREATE EXTENSION IF NOT EXISTS postgis;')

    return engine


def create_tables(flask_app):
    """Create the schema (all tables) as defined by {{cookiecutter.service_slug}}.models.

    Requires a flask application context to work.
    TODO - check for application context
    """
    db.create_all()


def drop_tables(flask_app):
    """Drop all tables defined by {{cookiecutter.service_slug}}.models.

    Requires a flask application context to work.
    TODO - check for application context
    """
    db.drop_all()