import errno
import os
import sys
from werkzeug.security import safe_str_cmp


def set_app_config():
    """APP_MODE; Valid values for this var are : dev, test or prod"""

    if os.path.isfile('/run/secrets/neo4j_db_user') and \
            os.path.isfile('/run/secrets/neo4j_db_password') and \
            os.path.isfile('/run/secrets/default_app_user_name') and \
            os.path.isfile('/run/secrets/default_app_user_password') and \
            os.path.isfile('/run/secrets/default_app_admin_name') and \
            os.path.isfile('/run/secrets/default_app_admin_password') and \
            os.path.isfile('/run/secrets/jwt_secret_key'):
        pass
    else:
        print("Secrets were not set")
        sys.exit(errno.EINTR)

    app_mode = os.environ.get('APP_MODE', default=None)

    if safe_str_cmp(app_mode, 'dev'):
        app_conf = DevelopmentConfig()
    elif safe_str_cmp(app_mode, 'test'):
        app_conf = TestingConfig()
    elif safe_str_cmp(app_mode, 'prod'):
        app_conf = ProductionConfig()
    else:
        print("APP_MODE env variable value should be: dev, test or prod")
        sys.exit(errno.EINTR)

    return app_conf


# All config keys not in UPPER CASE will be ignored by app.config.from_object
class Config(object):
    def __init__(self):
        file_neo4j_db_user = open("/run/secrets/neo4j_db_user", "r")
        file_neo4j_db_password = open("/run/secrets/neo4j_db_password", "r")
        file_jwt_secret_key = open("/run/secrets/jwt_secret_key", "r")

        self.neo4j_db_user = file_neo4j_db_user.read().strip()
        self.neo4j_db_password = file_neo4j_db_password.read().strip()
        self.DEBUG = False
        self.TESTING = False
        self.JWT_ALGORITHM = 'HS512'
        self.JWT_ACCESS_TOKEN_EXPIRES = 300  # 5 minutes
        self.JWT_REFRESH_TOKEN_EXPIRES = 43200  # 12 hours
        self.JWT_BLACKLIST_ENABLED = True
        self.JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
        self.JWT_SECRET_KEY = file_jwt_secret_key.read().strip()
        self.PROPAGATE_EXCEPTIONS = True
        self.REDIS_DB_SERVER = '172.17.0.1'
        self.NEO4J_DB_SERVER = '172.17.0.1'
        self.NEO4J_DB_CONN_STR = 'bolt://{user}:{password}@{db_server}:7687'

        file_jwt_secret_key.close()
        file_neo4j_db_user.close()
        file_neo4j_db_password.close()

    @property
    def NEO4J_DB_URL(self):
        return self.NEO4J_DB_CONN_STR.format(user=self.neo4j_db_user,
                                             password=self.neo4j_db_password,
                                             db_server=self.NEO4J_DB_SERVER)


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()

    NEO4J_DB_SERVER = '10.10.0.1'


class TestingConfig(Config):
    def __init__(self):
        super().__init__()

    TESTING = True
    NEO4J_DB_SERVER = '10.10.0.2'


class DevelopmentConfig(Config):
    def __init__(self,):
        super().__init__()

    DEBUG = True
