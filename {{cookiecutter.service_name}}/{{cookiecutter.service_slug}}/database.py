"""A Flask-SQLAlchemy database with a custom column type"""

from flask_sqlalchemy import sqlalchemy

from sqlalchemy_utils.functions import database_exists, create_database

from {{ cookiecutter.service_slug }} import alchemy

# import all modules here that might define models so that
# they will be registered properly on the metadata.
from {{ cookiecutter.service_slug }}.models import Base

db = alchemy


def setup_database(flask_app):
    with flask_app.app_context():

        engine = sqlalchemy.create_engine(
            flask_app.config['SQLALCHEMY_DATABASE_URI']
        )
        if not database_exists(engine.url):
            create_database(engine.url)

        create_tables()
        return True


def create_tables():
    Base.metadata.create_all(bind=db.engine)


def drop_tables():
    Base.metadata.drop_all(bind=db.engine)