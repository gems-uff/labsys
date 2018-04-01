from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from flask_admin import Admin


def setup_login_manager():
    login_manager = LoginManager()
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    return login_manager


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = setup_login_manager()
toolbar = DebugToolbarExtension()
admin = Admin(None, name='labsys', template_mode='bootstrap3')
