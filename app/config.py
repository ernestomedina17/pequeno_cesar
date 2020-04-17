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
        app_conf = DevelopmentConfig(jwt_secret_key, neo4_j_db_password)
    elif safe_str_cmp(app_mode, 'test'):
        app_conf = TestingConfig(jwt_secret_key, neo4_j_db_password)
    elif safe_str_cmp(app_mode, 'prod'):
        app_conf = ProductionConfig(jwt_secret_key, neo4_j_db_password)
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
    def __init__(self, jwt_secret_key, neo4_j_db_password):
        self.jwt_secret_key = jwt_secret_key
        self.neo4_j_db_password = neo4_j_db_password
        self.access_expires = 300  # 5 minutes
        self.refresh_expires = 43200  # 12 hours
        self.DEBUG = False
        self.TESTING = False
        self.JWT_ALGORITHM = 'HS512'
        self.JWT_ACCESS_TOKEN_EXPIRES = self.access_expires
        self.JWT_REFRESH_TOKEN_EXPIRES = self.refresh_expires
        self.JWT_BLACKLIST_ENABLED = True
        self.JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
        self.JWT_SECRET_KEY = jwt_secret_key
        self.PROPAGATE_EXCEPTIONS = True
        # Default Docker host network interface for inter container communication
        self.REDIS_DB_SERVER = '172.17.0.1'
        self.NEO4J_DB_SERVER = '172.17.0.1'
        self.NEO4J_DB_CONN_STR = 'bolt://neo4j:{password}@{db_server}:7687'

    @property
    def NEO4J_DB_URL(self):
        return self.NEO4J_DB_CONN_STR.format(password=self.neo4_j_db_password,
                                             db_server=self.NEO4J_DB_SERVER)


class ProductionConfig(Config):
    def __init__(self, jwt_secret_key, neo4_j_db_password):
        super().__init__(jwt_secret_key, neo4_j_db_password)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', default=None)
    NEO4J_DB_SERVER = '10.10.0.1'


class TestingConfig(Config):
    def __init__(self, jwt_secret_key, neo4_j_db_password):
        super().__init__(jwt_secret_key, neo4_j_db_password)
    TESTING = True
    NEO4J_DB_SERVER = '10.10.0.2'


class DevelopmentConfig(Config):
    def __init__(self, jwt_secret_key, neo4_j_db_password):
        super().__init__(jwt_secret_key, neo4_j_db_password)
    DEBUG = True
