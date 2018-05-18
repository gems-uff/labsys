from flask import Blueprint
from .models import Permission


blueprint = Blueprint('auth', __name__)


@blueprint.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
