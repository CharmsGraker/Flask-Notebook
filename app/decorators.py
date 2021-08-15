from functools import wraps
from flask import abort
from flask_login import current_user

from app.models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorate_function(*args,**kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args,**kwargs)
        return decorate_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)