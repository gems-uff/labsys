import unittest
from flask import current_app, url_for
from labsys import create_app, db
from labsys.models import *
from labsys.samples.forms import *


class TestForms(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.admission_valid_data = {

        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
