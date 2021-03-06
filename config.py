import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
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
    LOGIN_MESSAGE = 'É necessário realizar login para acessar essa página'

    PAGE_SIZE = 20

    UPLOAD_FOLDER = f'{BASEDIR}/labsys/tmp/csv/'
    ALLOWED_EXTENSIONS = {'csv'}

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SERVER_NAME = 'localhost.localdomain'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


class ProductionConfig(Config):
    BOOTSTRAP_SERVE_LOCAL = False
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
                fromaddr=cls.LABSYS_MAIL_SENDER,
                toaddrs=[cls.LABSYS_ADMIN],
                subject=cls.LABSYS_MAIL_SUBJECT_PREFIX + ' App Error',
                credentials=credentials,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    BOOTSTRAP_SERVE_LOCAL = False
    DEBUG = False
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}
