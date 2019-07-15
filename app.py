#!/usr/bin/env python3

from flask import Flask
from flask import request, make_response, jsonify
from flask_compress import Compress
from flask_cors import CORS
from flasgger import Swagger, swag_from

import logging

from config import get_config_by_env_mode, ProductionConfig
from api.routes import configure_api_routes
from api.error_handlers import configure_error_handlers


def configure_api(config=ProductionConfig):
    api = Flask(__name__)

    # Compress each response which content-length > 600
    Compress(api)

    _configure_api_doc(api, config)


    # Enable CORS headers on each api routes
    # CORS(api, allow_headers="Content-Type")


    configure_api_routes(api, config)

    configure_error_handlers(api, config)

    return api


def _configure_api_logging(api, config):
    if log_to_stdout:
        stream_handler = logging.StreamHandler()
        logging.root.addHandler(stream_handler)
    else:
        os.makedirs(LOG_DIR, exist_ok=True)
        logging.info('%s.log' % log_instance)
        formatter = RequestFormatter(
            '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
            '%(levelname)s in %(pathname)s: %(message)s'
        )


        my_file_handler.setFormatter(logging.Formatter(
            '%(asctime)s  %(remote_addr)s requested %(url)s\n%(levelname)s:[in :%(lineno)d] %(message)s '))
        logging.root.addHandler(my_file_handler)

    logging.root.setLevel(logging.INFO)
    logging.root.info('[Config] Logging : DONE ')


def _configure_api_doc(api, config):
    import json, collections

    # Import api basic info
    # with open("/api_info.json") as fp:
    # api_info = json.load(fp, object_pairs_hook=collections.OrderedDict)

    # Customize default configurations
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "/api/spec",
                "route": "/api/spec",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/api/doc",
    }

    swag_spec = Swagger(
        api, config=swagger_config, template_file="api/swagger/template_api_info.yml"
    )

    return swag_spec




if __name__ == "__main__":
    Config = get_config_by_env_mode()
    app = configure_api(Config)
    app.run(debug=Config.DEBUG, host="0.0.0.0")
