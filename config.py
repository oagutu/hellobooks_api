"""
config.py
Specifies default environment settings.
"""

from os import urandom


class Config(object):
    """
    Main config class."""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = urandom(24)


class TestingConfig(Config):
    """Testing config settings"""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@postgresadmin@localhost/hb_test_db'


class DevelopmentConfig(Config):
    """
    Development config settings."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@postgresadmin@localhost/hb_dev_db'


class ProductionConfig(Config):
    """
    Production config settings."""

    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
