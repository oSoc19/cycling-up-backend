from dotenv import load_dotenv

import os
from pathlib import Path


ENV_PATH = Path('.') / '.env'
load_dotenv(dotenv_path=ENV_PATH)


_BASE_DIR = Path(__file__).parent
_DEFAULT_DATA_DIR = os.path.join(_BASE_DIR, "data")
_DEFAULT_LOG_DIR = os.path.join(_BASE_DIR, "logs")


class Config(object):
    ENV = os.getenv("FLASK_ENV", default="production")
    DEBUG = os.getenv("DEBUG", default="false").lower() in {"1", "t", "true"}
    DATA_DIR = os.getenv("DATA_DIR", default=_DEFAULT_DATA_DIR)
    LOG_DIR = os.getenv("LOG_DIR", default=_DEFAULT_LOG_DIR)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


CONFIG_BY_NAME = dict(dev=DevelopmentConfig, prod=ProductionConfig)

def get_config_by_env_mode():
    is_mode_dev = Config.ENV != "production"
    return CONFIG_BY_NAME["dev"] if is_mode_dev else CONFIG_BY_NAME["prod"]
