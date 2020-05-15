import errno
import os
import sys
import base64
from werkzeug.security import safe_str_cmp
from cryptography.fernet import Fernet


def set_app_config():
    """APP_MODE; Valid values for this var are : dev, test or prod"""

    if os.path.isfile('/run/secrets/neo4j_db_user') and \
            os.path.isfile('/run/secrets/neo4j_db_password') and \
            os.path.isfile('/run/secrets/default_app_user_name') and \
            os.path.isfile('/run/secrets/default_app_user_password') and \
            os.path.isfile('/run/secrets/default_app_admin_name') and \
            os.path.isfile('/run/secrets/default_app_admin_password') and \
            os.path.isfile('/run/secrets/jwt_secret_key') and \
            os.path.isfile('/run/secrets/encryption_key'):
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
        # Secret files
        file_encryption_key = open(os.path.expanduser('/run/secrets/encryption_key'), 'rb')
        encryption_key = file_encryption_key.read()
        file_encryption_key.close()
        fer = Fernet(encryption_key)

        file_neo4j_db_user = open("/run/secrets/neo4j_db_user", "rb")
        file_neo4j_db_password = open("/run/secrets/neo4j_db_password", "rb")
        file_jwt_secret_key = open("/run/secrets/jwt_secret_key", "rb")

        # Decrypt
        decrypted_neo4j_db_user = fer.decrypt(file_neo4j_db_user.read())
        decrypted_neo4j_db_password = fer.decrypt(file_neo4j_db_password.read())
        decrypted_jwt_secret_key = fer.decrypt(file_jwt_secret_key.read())

        # Base64 Decode
        decoded_neo4j_db_user = base64.b64decode(decrypted_neo4j_db_user)
        decoded_neo4j_db_password = base64.b64decode(decrypted_neo4j_db_password)
        decoded_jwt_secret_key = base64.b64decode(decrypted_jwt_secret_key)

        # UTF-8 Decode
        decoded_neo4j_db_user = decoded_neo4j_db_user.decode()
        decoded_neo4j_db_password = decoded_neo4j_db_password.decode()
        decoded_jwt_secret_key = decoded_jwt_secret_key.decode()

        file_neo4j_db_user.close()
        file_neo4j_db_password.close()
        file_jwt_secret_key.close()

        self.neo4j_db_user = decoded_neo4j_db_user.strip()
        self.neo4j_db_password = decoded_neo4j_db_password.strip()
        self.DEBUG = False
        self.TESTING = False
        self.JWT_ALGORITHM = 'HS512'
        self.JWT_ACCESS_TOKEN_EXPIRES = 300  # 5 minutes
        self.JWT_REFRESH_TOKEN_EXPIRES = 43200  # 12 hours
        self.JWT_BLACKLIST_ENABLED = True
        self.JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
        self.JWT_SECRET_KEY = decoded_jwt_secret_key.strip()
        self.PROPAGATE_EXCEPTIONS = True
        self.REDIS_DB_SERVER = '172.17.0.1'
        self.NEO4J_DB_SERVER = '172.17.0.1'
        self.NEO4J_DB_CONN_STR = 'bolt://{user}:{password}@{db_server}:7687'

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
