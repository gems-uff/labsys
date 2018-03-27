from functools import wraps
from flask import abort, current_app
from flask_login import current_user
from labsys.auth.models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission) and \
                not current_app.config['TESTING'] == True:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER) (f)
