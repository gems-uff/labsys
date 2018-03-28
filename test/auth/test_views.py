import os, unittest
from flask import url_for

from labsys.app import create_app, db
from labsys.auth.models import Role
import labsys.inventory.models as models


class TestAuthenticationViews(unittest.TestCase):

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

    def test_register_and_login(self):
        response = self.client.post(url_for('auth.register'), data={
            'email': 'a@a.com',
            'password': 'a',
            'password2': 'a',
        })
        self.assertEqual(response.status_code, 302)
