# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('LABSYS_SECRET', 'couldnotfindsecretkey')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    # Databases URL changed by active environment
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEBPACK_MANIFEST_PATH = 'webpack/manifest.json'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # Commit after request finished
    SSL_DISABLE = True  # Must be overriden by Prod and Heroku
    BOOTSTRAP_SERVE_LOCAL = True

    # Email configuration
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    LABSYS_ADMIN_MAIL = 'gabrielcrsaldanha@gmail.com'
    LABSYS_MAIL_SUBJECT_PREFIX = '[LabSys]'
    LABSYS_MAIL_SENDER = 'LabSys Admin <gabrielcrsaldanha@gmail.com>'


# TODO: Create Heroku specific config class -> ProdConfig

class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    SSL_DISABLE = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False  # Allows form testing
