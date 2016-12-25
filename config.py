import os

class Config(object):
    """
    Common configurations
    """
    SECRET_KEY = 'eduard_78d'

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/twitter'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

class TestingConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/twitter_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}


