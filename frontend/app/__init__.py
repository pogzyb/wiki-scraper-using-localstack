import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger(__name__).setLevel(logging.DEBUG)

login = LoginManager()
db = SQLAlchemy()


def create_app():
    """
    Factory function sits atop the application
    :return: Flask application
    """
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object('config.ProductionConfig')
    elif env == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    login.init_app(app)
    login.blueprint_login_views = {'auth': '/login'}

    db.init_app(app)

    from app.blueprints.auth.email import me
    me.init_app()

    with app.app_context():
        from app.blueprints import api, auth, web
        app.register_blueprint(web)
        app.register_blueprint(api)
        app.register_blueprint(auth)

        db.create_all()

    return app
