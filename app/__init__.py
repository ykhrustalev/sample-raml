import os

from flask import Flask

from .models import db
from .resources import routes

__all__ = [
    'config',
    'resources',
    'schemas',
    'models',
]


def create_app():
    app = Flask('app')
    app.url_map.strict_slashes = False

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']

    db.init_app(app)
    with app.app_context():
        db.create_all()

    routes(app)

    return app
