from flask import Flask, render_template

from config import CONFIG

from .main.views import blueprint as main_blueprint
from .admissions.views import blueprint as admissions_blueprint
from .auth.views import blueprint as auth_blueprint
from .inventory.views import blueprint as inventory_blueprint
from .extensions import (
    bootstrap, mail, moment, db, login_manager, toolbar, admin,
)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    return app


def register_extensions(app):
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)
    admin.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(inventory_blueprint, url_prefix='/inventory')
    app.register_blueprint(admissions_blueprint, url_prefix='/admissions')


def register_error_handlers(app):
    @app.errorhandler(403)
    def unauthorized(e):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
