import os, unittest
from flask import url_for

from labsys.app import create_app, db
from labsys.auth.models import Role
import labsys.inventory.models as models


class TestInventoryViews(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
