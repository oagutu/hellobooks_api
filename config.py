'''instance/config.py
specifies default environment settings'''

import os


class Config(object):
    '''main config class'''

    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = "oj3099834$#!)_(efqkp-034r9jp4jorfpo//2_$@*epok"


class DevelopmentConfig(Config):
    '''development config settings'''
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
