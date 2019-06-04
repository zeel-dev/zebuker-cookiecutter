# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from logging.config import dictConfig

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import connexion

from {{ cookiecutter.service_slug }}.config import LocalhostConfig

# Instantiate extensions core to our application
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()


def create_app(config_object=LocalhostConfig):
    """Create an instance of Connexion with a particular configuration.

    See details here for a flask factory patter approach
    http://flask.pocoo.org/docs/patterns/appfactories/.

    Parameters
    ----------
    config_object : Config
        A particular config defined by the service.
    """

    # Create connexion instance
    app = connexion.App(__name__, specification_dir='../')

    # Configure underlying flask app and configure it
    flask_app = app.app
    flask_app.config.from_object(config_object)

    # Register loggers with flask app
    register_loggers(flask_app)

    # Register extensions with flask app
    register_extensions(flask_app)

    # Register swagger defined api endpoints
    register_endpoints(app)
    return app


def register_endpoints(app):
    """Register endpoints defined in openapi.yml

    Additionally register any flask endpoints / blueprints

    Parameters
    ----------
    app : Connexion
        A Connexion application instance.
    """
    app.add_api('openapi.yml', strict_validation=True)

    # Add health check
    @app.app.route('/health/pricing')
    def health_check():
        """Pingable endpoint used to determine whether the service is running
        """
        return '', 200


def register_extensions(app):
    """Register Flask extensions.

    Parameters
    ----------
    app : Flask
        A flask application instance.
    """
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})


def register_loggers(app):
    """Initialize loggers defined in flask app config with dictConfig

    Parameters
    ----------
    app : Flask
        A flask application instance
    """

    dictConfig(app.config.get('LOG_CONFIG'))