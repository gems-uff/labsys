import unittest
from labsys.app import create_app

class TestConfig(unittest.TestCase):

    def test_production_config(self):
        app = create_app('production')
        self.assertFalse(app.testing)
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['BOOTSTRAP_SERVE_LOCAL'])

    def test_heroku_config(self):
        app = create_app('heroku')
        self.assertFalse(app.testing)
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['BOOTSTRAP_SERVE_LOCAL'])

    def test_development_config(self):
        app = create_app('development')
        self.assertTrue(app.config['DEBUG'])

    def test_testing_config(self):
        app = create_app('testing')
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(app.testing)