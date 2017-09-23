from flask import Flask

from config import config

from .main.views import blueprint as main_blueprint
from .admissions.views import blueprint as admissions_blueprint
from .auth.views import blueprint as auth_blueprint
from .inventory.views import blueprint as inventory_blueprint
from .extensions import bootstrap, mail, moment, db, login_manager


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(inventory_blueprint, url_prefix='/inventory')
    app.register_blueprint(admissions_blueprint, url_prefix='/admissions')
