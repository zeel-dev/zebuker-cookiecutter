import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Init Flask App
flask_app = Flask(__name__)

CORS(flask_app, resources={r"/*": {"origins": "*"}})

# Configure Flask App Instance
flask_config_string = os.environ.get(
    'FLASK_CONFIG_CLASS',
    'pricing.config.LocalhostConfig'
)
flask_app.config.from_object(flask_config_string)

# Configure Flask-SQLAlchemy
alchemy = SQLAlchemy()
alchemy.init_app(flask_app)
