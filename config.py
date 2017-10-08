import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SSL_DISABLE = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    LABSYS_ADMIN = os.environ.get('LABSYS_ADMIN', '')
    LABSYS_MAIL_SUBJECT_PREFIX = '[LabSys]'
    LABSYS_MAIL_SENDER = 'LabSys Admin <{}>'.format(LABSYS_ADMIN)

    BOOTSTRAP_SERVE_LOCAL = True


class DevelopmentConfig(Config):
    DEBUG = True
    BOOTSTRAP_SERVE_LOCAL = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    BOOTSTRAP_SERVE_LOCAL = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    BOOTSTRAP_SERVE_LOCAL = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class HerokuConfig(ProductionConfig):
    BOOTSTRAP_SERVE_LOCAL = False
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}
