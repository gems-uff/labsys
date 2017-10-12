import os

from labsys.app import create_app


def test_production_config():
    app = create_app('production')
    assert app.config['DATABASE_URI_ENV_KEY'] == 'DATABASE_URL'
    assert app.config['DEBUG'] is False

def test_development_config():
    app = create_app('development')
    assert app.config['DATABASE_URI_ENV_KEY'] == 'DEV_DATABASE_URL'
    assert app.config['DEBUG'] is True

def test_testing_config():
    app = create_app('testing')
    assert app.config['DATABASE_URI_ENV_KEY'] == 'TEST_DATABASE_URL'
    assert app.config['TESTING'] is True
