import os, unittest
from labsys.app import create_app

class TestConfig(unittest.TestCase):

    def test_production_config(self):
        app = create_app('production')
        self.assertEqual(app.config['DATABASE_URI_ENV_KEY'], 'DATABASE_URL')
        self.assertFalse(app.config['DEBUG'])


    def test_development_config(self):
        app = create_app('development')
        self.assertEqual(app.config['DATABASE_URI_ENV_KEY'], 'DEV_DATABASE_URL')
        self.assertTrue(app.config['DEBUG'])


    def test_testing_config(self):
        app = create_app('testing')
        self.assertEqual(app.config['DATABASE_URI_ENV_KEY'], 'TEST_DATABASE_URL')
        self.assertTrue(app.config['TESTING'])