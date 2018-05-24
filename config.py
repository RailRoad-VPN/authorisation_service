class Config(object):
    DEBUG = False
    TESTING = False

    APP_SESSION_SK = 'dMMArRPsYZdxQe2ZKen'
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = APP_SESSION_SK
    TEMPLATES_AUTO_RELOAD = True

    VERSION = 'v1'
    API_BASE_URI = '/api/%s' % VERSION


class ProductionConfig(Config):
    PSQL_DBNAME = 'rrnauth'
    PSQL_USER = 'railroadman'
    PSQL_PASSWORD = ''
    PSQL_HOST = ''


class DevelopmentConfig(Config):
    DEBUG = True

    PSQL_DBNAME = 'rrnauth'
    PSQL_USER = 'railroadman'
    PSQL_PASSWORD = 'railroadman'
    PSQL_HOST = '127.0.0.1'


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
