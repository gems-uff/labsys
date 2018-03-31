import logging
from flask import Blueprint
from labsys.auth.decorators import restrict_to_logged_users

logging.basicConfig(level=logging.INFO)
logger = logging
blueprint = Blueprint('inventory', __name__)
blueprint.before_request(restrict_to_logged_users)
