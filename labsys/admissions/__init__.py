import logging

from flask import Blueprint

from labsys.auth.decorators import restrict_to_logged_users

logger = logging.basicConfig(level=logging.INFO)
blueprint = Blueprint('admissions', __name__)
blueprint.before_request(restrict_to_logged_users)
