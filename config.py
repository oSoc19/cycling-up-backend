from dotenv import load_dotenv

import os
from pathlib import Path


ENV_PATH = Path('.') / '.env'
load_dotenv(dotenv_path=ENV_PATH)


_BASE_DIR = Path(__file__).parent
_DEFAULT_LOG_DIR = os.path.join(_BASE_DIR, "logs")
_DEFAULT_DATA_DIR = os.path.join(_BASE_DIR, "data")
_DEFAULT_MOBIGIS_DIR = os.path.join(_DEFAULT_DATA_DIR, "fetch_mobigis")
_DEFAULT_HISTORICAL_DIR = os.path.join(_DEFAULT_DATA_DIR, "historical")
_DEFAULT_INFRA_DATES_DIR = os.path.join(_DEFAULT_DATA_DIR, "construction_date")


class Config(object):
    ENV = os.getenv("FLASK_ENV", default="production")
    DEBUG = os.getenv("DEBUG", default="false").lower() in {"1", "t", "true"}
    DATA_DIR = os.getenv("DATA_DIR", default=_DEFAULT_DATA_DIR)
    LOG_DIR = os.getenv("LOG_DIR", default=_DEFAULT_LOG_DIR)
    MOBIGIS_DIR = os.getenv("MOBIGIS_DIR", default=_DEFAULT_MOBIGIS_DIR)
    HISTORICAL_DIR = os.getenv("HISTORICAL_DIR", default=_DEFAULT_HISTORICAL_DIR)
    INFRA_DATES_DIR = os.getenv("INFRA_DATES_DIR", default=_DEFAULT_INFRA_DATES_DIR)


    def init_dirs(self):
        dir_attrs = [d for d in dir(self) if d.endswith('_DIR') ]

        for attr in dir_attrs:
            dir_name = getattr(self, attr)
            os.makedirs(dir_name,exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


CONFIG_BY_NAME = dict(dev=DevelopmentConfig(), prod=ProductionConfig())

def get_config_by_env_mode():
    is_mode_dev = Config.ENV != "production"
    return CONFIG_BY_NAME["dev"] if is_mode_dev else CONFIG_BY_NAME["prod"]


