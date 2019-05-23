"""Static definitions module (constants)"""
import os

PRECISION_LAT = 6
PRECISION_LNG = 6

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, '../resources')

SERVICE_NAME = '{{cookiecutter.service_slug}}'
