from flask import (
    render_template,
    Blueprint,
)

blueprint = Blueprint('main', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')
