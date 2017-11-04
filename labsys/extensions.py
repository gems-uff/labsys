from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from playhouse.flask_utils import FlaskDB


def setup_login_manager():
    login_manager = LoginManager()
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    return login_manager


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
database = FlaskDB()
login_manager = setup_login_manager()
