from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../settings.py')
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    db.init_app(app)

    return app

