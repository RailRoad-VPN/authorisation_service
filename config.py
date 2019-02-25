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
    ENV = 'production'
    PSQL_DBNAME = 'rrnauth'
    PSQL_USER = 'railroadman'
    PSQL_PASSWORD = ''
    PSQL_HOST = ''


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

    PSQL_DBNAME = 'rrnauth'
    PSQL_USER = 'railroadman'
    PSQL_PASSWORD = 'railroadman'
    PSQL_HOST = '127.0.0.1'

    USER_TICKET_ZIP_DIR = '/Users/dikkini/Downloads'


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    DEBUG = True

    PSQL_DBNAME = 'rrnauth'
    PSQL_USER = 'railroadman'
    PSQL_PASSWORD = 'railroadman'
    PSQL_HOST = '127.0.0.1'

    USER_TICKET_ZIP_DIR = '/opt/apps/dfn/tickets'
