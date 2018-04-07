from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user
from labsys.auth.models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


def restrict_to_logged_users():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
