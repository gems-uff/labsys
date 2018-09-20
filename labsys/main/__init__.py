
import os

from .views import blueprint


@blueprint.app_context_processor
def inject_permissions():
    show_labsys = not os.environ.get('SHOW_LABSYS') == 'False'
    return dict(show_labsys=show_labsys)
