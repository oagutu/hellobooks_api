"""
config.py
Specifies default environment settings.
"""


class Config(object):
    """
    Main config class."""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = "oj3099834$#!)_(efqkp-034r9jp4jorfpo//2_$@*epok"


class DevelopmentConfig(Config):
    """
    Development config settings."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@postgresadmin@localhost/hb_test_db'


class ProductionConfig(Config):
    """
    Production config settings."""

    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
