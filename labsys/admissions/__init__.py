from flask import Blueprint
from labsys.auth.decorators import restrict_to_logged_users

blueprint = Blueprint('admissions', __name__)
blueprint.before_request(restrict_to_logged_users)
