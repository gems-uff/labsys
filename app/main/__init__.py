from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from app.auth.models import Permission


@main.app_context_processor
def inject_permissions():
    """This function is executed each request,
    even though outside of the bluprint"""
    return dict(Permission=Permission)
