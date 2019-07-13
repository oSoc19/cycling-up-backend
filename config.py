import os

_BASE_DIR = Path(__file__).parent
_DATA_DIR = os.path.join(_BASE_DIR, "data")


class Config(object):
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)

