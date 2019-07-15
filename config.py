import os
from pathlib import Path


_BASE_DIR = Path(__file__).parent
_DEFAULT_DATA_DIR = os.path.join(_BASE_DIR, "data")
_DEFAULT_LOG_DIR = os.path.join(_BASE_DIR.parent, "logs")


class Config(object):
    ENV = os.getenv("FLASK_ENV", default="production")
    DEBUG = os.getenv("DEBUG", default="false").lower() in {"1", "t", "true"}
    DATA_DIR = os.getenv("DATA_DIR", default=_DEFAULT_DATA_DIR)
    LOG_DIR = os.getenv("LOG_DIR", default=_DEFAULT_LOG_DIR)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(dev=DevelopmentConfig, prod=ProductionConfig)

