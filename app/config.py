import errno
import os
import sys
from werkzeug.security import safe_str_cmp


def set_app_config():
    """Ensure the following ENV variables are set, otherwise exit the application
    JWT_SECRET_KEY; String to encrypt tokens
    NEO4J_DB_PASSWORD; String password of neo4j user
    APP_MODE; Values may be: dev, test or prod
    """

    app_mode = os.environ.get('APP_MODE', default=None)
    jwt_secret_key = os.environ.get('JWT_SECRET_KEY', default=None)
    neo4_j_db_password = os.environ.get('NEO4J_DB_PASSWORD', default=None)

    if safe_str_cmp(app_mode, 'dev'):
        app_conf = DevelopmentConfig
    elif safe_str_cmp(app_mode, 'test'):
        app_conf = TestingConfig
    elif safe_str_cmp(app_mode, 'prod'):
        app_conf = ProductionConfig
    elif jwt_secret_key is None or neo4_j_db_password is None or app_mode is None:
        # TODO: implement logging to file
        print("Env variable(s) not set")
        sys.exit(errno.EINTR)
    else:
        print("APP_MODE value should be one of: dev, test or prod")
        sys.exit(errno.EINTR)

    return app_conf


# All config keys not in UPPER CASE will be ignored by app.config.from_object
class Config(object):
    access_expires = 300  # 5 minutes
    refresh_expires = 43200  # 12 hours
    DEBUG = False
    TESTING = False
    JWT_ALGORITHM = 'HS512'
    JWT_ACCESS_TOKEN_EXPIRES = access_expires
    JWT_REFRESH_TOKEN_EXPIRES = refresh_expires
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = True
    # Default Docker host network interface for inter container communication
    REDIS_DB_SERVER = '172.17.0.1'
    NEO4J_DB_SERVER = '172.17.0.1'
    NEO4J_DB_CONN_STR = 'bolt://neo4j:{password}@{db_server}:7687'

    @property
    def NEO4J_DB_URL(self):
        return self.NEO4J_DB_CONN_STR.format(password=os.environ.get('NEO4J_DB_PASSWORD', default=None),
                                             db_server=self.NEO4J_DB_SERVER)


class ProductionConfig(Config):
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', default=None)
    NEO4J_DB_SERVER = '10.10.0.1'


class TestingConfig(Config):
    TESTING = True
    NEO4J_DB_SERVER = '10.10.0.2'


class DevelopmentConfig(Config):
    DEBUG = True
