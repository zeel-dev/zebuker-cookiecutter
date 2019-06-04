"""Run script meant for starting Flask app"""
import logging
import os
import time

from flask_migrate import upgrade

import {{cookiecutter.service_slug}}.config as config_classes
from {{cookiecutter.service_slug}} import create_app
from {{cookiecutter.service_slug}}.helpers.database import create_database


def get_flask_config_class():
    flask_env = os.environ.get('FLASK_ENV')
    if flask_env == 'PROD' or flask_env == 'QA' or flask_env == 'DEV':
        return config_classes.FargateConfig

    return config_classes.LocalhostConfig


if __name__ == '__main__':

    # Figure out which config to instantiate Connexion with
    config_class = get_flask_config_class()

    # Create connexion app
    connexion = create_app(config_class)
    flask_app = connexion.app

    # Create application context
    app_ctx = flask_app.app_context()
    app_ctx.push()

    config = flask_app.config

    # Only create resources for LocalhostConfig and only on initial thread.
    if (
        config.get('CONFIG_NAME') == config_classes.LocalhostConfig.CONFIG_NAME
        and os.environ.get('WERKZEUG_RUN_MAIN') is None
    ):

        logger = logging.getLogger('startup')
        logger.info('Creating Resources')

        database_created = False
        while not database_created:
            try:
                logger.info('Creating database...')
                create_database(flask_app)
                upgrade()
                database_created = True
                logger.info('Database created')
            except Exception:
                logger.exception('Unable to create database')
                time.sleep(3)

    # Start connextion app
    connexion.run(
        debug=config.get('DEBUG'),
        port=5000,
        host='0.0.0.0'
    )


