from flask import Blueprint

samples = Blueprint('samples', __name__)

from . import views, errors
from labsys.auth.models import Permission


@samples.app_context_processor
def inject_permissions():
    """This function is executed each request,
    even though outside of the bluprint"""
    return dict(Permission=Permission)
