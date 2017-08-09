# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from labsys.app import create_app
from labsys.settings import DevConfig, ProdConfig

# get_debug_flag tries to find FLASK_DEBUG defined in path
CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
