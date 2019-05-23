#!/usr/bin/env python
from random import randint
import os
import time

from {{cookiecutter.service_slug}} import flask_app
from {{cookiecutter.service_slug}}.database import setup_database
from zeel_utils.logger_utils import create_logger

logger = create_logger('startup')

if __name__ == '__main__':

    # Only create resources on initial thread
    if os.environ.get('WERKZEUG_RUN_MAIN') is None:

        config = flask_app.config
        logger.info('Creating Resources')

        database_created = False
        while not (database_created):
            time.sleep(randint(5, 15))
            if not database_created:
                try:
                    logger.info('Creating database...')
                    database_created = setup_database(flask_app)
                    logger.info('Database created')
                except Exception as exception:
                    logger.error(exception)

    flask_app.run('0.0.0.0', 5000)

