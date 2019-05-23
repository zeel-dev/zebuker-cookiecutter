import os

import {{cookiecutter.service_slug}}.definitions as definitions


class Config(object):
    DEBUG = False
    TESTING = False
    POSTGRESQL_DATABASE_USER = 'root'
    POSTGRESQL_DATABASE_PASS = 'root'
    POSTGRESQL_DATABASE_NAME = '{{cookiecutter.database}}'
    POSTGRESQL_DATABASE_HOST = 'db'
    SERVICE_NAME = definitions.SERVICE_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalhostConfig(Config):
    POSTGRESQL_DATABASE_HOST_URI = 'postgresql://{}:{}@{}'.format(
        Config.POSTGRESQL_DATABASE_USER,
        Config.POSTGRESQL_DATABASE_PASS,
        Config.POSTGRESQL_DATABASE_HOST
    )
    SQLALCHEMY_DATABASE_URI = '{}/{}'.format(
        POSTGRESQL_DATABASE_HOST_URI,
        Config.POSTGRESQL_DATABASE_NAME
    )

    DEBUG = True


class TestingConfig(Config):
    """Flask config to use when running unit tests
    """
    CONFIG_NAME = 'TestingConfig'

    # Flask Config
    # ------------
    TESTING = True

    # MySQL Settings
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


class TravisConfig(Config):
    """Flask config to use when running in travis.
    Used for running migrations primarily.
    """
    CONFIG_NAME = 'TravisConfig'

    # Flask Config
    # ------------
    DEBUG = True

    # MySQL Settings
    # --------------
    MYSQL_DATABASE_USER = os.environ.get('MYSQL_DATABASE_USER')
    MYSQL_DATABASE_PASS = os.environ.get('MYSQL_DATABASE_PASS')
    MYSQL_DATABASE_HOST = os.environ.get('MYSQL_DATABASE_HOST')
    POSTGRESQL_DATABASE_HOST_URI = 'postgresql://{}:{}@{}'.format(
        Config.POSTGRESQL_DATABASE_USER,
        Config.POSTGRESQL_DATABASE_PASS,
        Config.POSTGRESQL_DATABASE_HOST
    )
    SQLALCHEMY_DATABASE_URI = '{}/{}'.format(
        POSTGRESQL_DATABASE_HOST_URI,
        Config.POSTGRESQL_DATABASE_NAME
    )