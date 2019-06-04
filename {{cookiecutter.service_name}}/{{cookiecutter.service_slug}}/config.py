"""Safe defaults for Flask app configuration"""
import os

import {{cookiecutter.service_slug}}.definitions as definitions

IN_DOCKER = os.environ.get('IN_DOCKER')


class Config(object):
    """Base class for all flask configurations"""

    # Flask config
    # ------------
    DEBUG = False
    TESTING = False

    # Flask-sqlalchemy config
    # -----------------------
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging
    # -------
    LOG_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'named_standard': {
                'format': '[%(asctime)s] %(name)s - %(levelname)s in '
                '%(module)s: %(message)s',
            },
            'standard': {
                'format': '[%(asctime)s] %(levelname)s in '
                '%(module)s: %(message)s',
            },
        },
        'handlers': {
            'console_handler': {
                'level': 'INFO',
                'formatter': 'named_standard',
                'class': 'logging.StreamHandler',
            },
            'file_handler_flask': {
                'level': 'INFO',
                'filename': 'log/flask.log',
                'class': 'logging.FileHandler',
                'formatter': 'standard'
            },
            'file_handler_startup': {
                'level': 'INFO',
                'filename': 'log/startup.log',
                'class': 'logging.FileHandler',
                'formatter': 'standard'
            }
        },
        'loggers': {
            'alembic': {
                'handlers': [
                    'console_handler',
                    'file_handler_startup'
                ],
                'level': 'INFO',
                'propagate': True
            },
            'flask.app': {
                'handlers': [
                    'console_handler',
                    'file_handler_flask'
                ],
                'level': 'INFO',
                'propagate': True
            },
            'startup': {
                'handlers': [
                    'console_handler',
                    'file_handler_startup'
                ],
                'level': 'INFO',
                'propagate': True
            },
            'werkzeug': {
                'handlers': [
                    'console_handler'
                ],
                'level': 'ERROR',
                'propagate': True
            }
        }
    }

    # Postgresql Settings
    # -------------------
    POSTGRESQL_DATABASE_USER = 'root'
    POSTGRESQL_DATABASE_PASS = 'root'
    POSTGRESQL_DATABASE_NAME = '{{cookiecutter.database}}'
    POSTGRESQL_DATABASE_HOST = 'db' if IN_DOCKER else 'localhost'

    # Service specific settings
    # -------------------------
    SERVICE_NAME = definitions.SERVICE_NAME


class FargateConfig(Config):
    """Flask config to use when deployed to Fargate.

    Database should be external to the docker environment and credentials
    should be supplied via environment variables. Debug mode is also exposed as
    an env variable.
    """
    CONFIG_NAME = 'FargateConfig'

    # Flask config
    # ------------
    DEBUG = os.environ.get('DEBUG', False)

    # Postgresql Settings
    # -------------------
    POSTGRESQL_DATABASE_USER = os.environ.get('POSTGRESQL_DATABASE_USER')
    POSTGRESQL_DATABASE_PASS = os.environ.get('POSTGRESQL_DATABASE_PASS')
    POSTGRESQL_DATABASE_HOST = os.environ.get('POSTGRESQL_DATABASE_HOST')
    POSTGRESQL_DATABASE_HOST_URI = 'postgresql://{}:{}@{}'.format(
        POSTGRESQL_DATABASE_USER,
        POSTGRESQL_DATABASE_PASS,
        POSTGRESQL_DATABASE_HOST
    )
    SQLALCHEMY_DATABASE_URI = '{}/{}'.format(
        POSTGRESQL_DATABASE_HOST_URI,
        Config.POSTGRESQL_DATABASE_NAME
    )


class LocalhostConfig(Config):
    """Flask config when run locally. The default option.

    Database should be internal to the docker environment and credentials
    should be the default values in Config.
    """
    CONFIG_NAME = 'LocalhostConfig'

    # Flask config
    # ------------
    DEBUG = True

    # Postgresql Settings
    # -------------------
    POSTGRESQL_DATABASE_HOST_URI = 'postgresql://{}:{}@{}'.format(
        Config.POSTGRESQL_DATABASE_USER,
        Config.POSTGRESQL_DATABASE_PASS,
        Config.POSTGRESQL_DATABASE_HOST
    )
    SQLALCHEMY_DATABASE_URI = '{}/{}'.format(
        POSTGRESQL_DATABASE_HOST_URI,
        Config.POSTGRESQL_DATABASE_NAME
    )


class TestingConfig(Config):
    """Flask config to use when running unit tests.

    Database should be internal to the docker environment and credentials
    should be the default values in Config.
    """
    CONFIG_NAME = 'TestingConfig'

    # Flask Config
    # ------------
    TESTING = True

    # Postgresql Settings
    # --------------
    POSTGRESQL_DATABASE_NAME = 'test_{}'.format(
        Config.POSTGRESQL_DATABASE_NAME
    )
    POSTGRESQL_DATABASE_HOST_URI = 'postgresql://{}:{}@{}'.format(
        Config.POSTGRESQL_DATABASE_USER,
        Config.POSTGRESQL_DATABASE_PASS,
        Config.POSTGRESQL_DATABASE_HOST
    )
    SQLALCHEMY_DATABASE_URI = '{}/{}'.format(
        POSTGRESQL_DATABASE_HOST_URI,
        POSTGRESQL_DATABASE_NAME
    )
