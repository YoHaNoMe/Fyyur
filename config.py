import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Upload folder
UPLOAD_FOLDER = 'static/img'

# TODO IMPLEMENT DATABASE URL (Completed)
# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgres:///fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = True
