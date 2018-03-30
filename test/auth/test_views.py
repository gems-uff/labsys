import unittest
from flask import url_for, request

from labsys.app import create_app, db
from labsys.auth.models import Role, User


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
        # register a new account
        response = self.client.post(url_for('auth.register'), data={
            'email': 'a@a.com',
            'password': 'a',
            'password2': 'a',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensagem de confirmação foi enviado para seu email',
                      response.get_data(as_text=True))

        # login using new account redirects to confirmation page
        response = self.client.post(url_for('auth.login'), data={
            'email': 'a@a.com',
            'password': 'a',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        self.assertIn('Você ainda não confirmou sua conta', data)

        # confirm account by token
        user = User.query.filter_by(email='a@a.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Conta verificada', data)

        # log in effectively goes to Index stock page
        with self.client as client:
            response = client.post(url_for('auth.login'), data={
                'email': 'a@a.com',
                'password': 'a',
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.path, '/inventory/stock')

        # log out
