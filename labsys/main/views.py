import os

from flask import (
    render_template,
    Blueprint,
    redirect
)

blueprint = Blueprint('main', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return redirect(os.environ.get('SMS_URL'))
