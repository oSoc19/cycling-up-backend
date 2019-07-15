#!/usr/bin/env python3

from flask import Flask
from flask import request, make_response, jsonify
from flask_compress import Compress
from flask_cors import CORS
from flasgger import Swagger, swag_from


import api.getters as getters


api = Flask(__name__)

# Compress each response which content-length > 600
Compress(api)

# Enable CORS headers on each api routes
CORS(api, allow_headers="Content-Type")


@api.route("/")
@api.route("/api/ping")
@swag_from("api/swagger/get_ping.yml")
def api_ping():
    """
    Route to check the connectivity
    """
    return jsonify(message="Yello World !")


@api.route("/api/map/historical/<int:year>")
@swag_from("api/swagger/get_map_historical.yml")
def getMapHistorical(year):
    """
    Get the historical map
    """

    return jsonify(getters.getMatchedFeaturesHistorical(year))


@api.route("/api/map/general/<string:kind>")
@swag_from("api/swagger/get_map_general.yml")
def getGeneralMap(kind):
    """
    Retrieve the general map
    """

    data = getters.getJsonContents(kind)
    if data is not None:
        return jsonify(data)
    else:
        return _not_found()

@api.route("/api/map/live_bike/<string:kind>")
@swag_from("api/swagger/get_map_bike_count.yml")
def getLiveBikeCount(kind):
    """
    Retrieve live bike count data or GFR map.
    """
    if kind == "count":
        data = getters.getBikeCount()
        return jsonify(data)
    elif kind == "GFR":
        data = getters.getJsonContents("bike_icr")
        return jsonify(data)
    else:
        return _not_found()


@api.route("/api/map/villo/<string:kind>")
@swag_from("api/swagger/get_villo_data.yml")
def getVilloData(kind):
    """
    Retrieve villo information as requested by 'kind'.
    """
    if kind == "stations":
        data = getters.getJsonContents("bike_villo")
        return jsonify(data)
    elif kind == "live":
        data = getters.getLiveVilloData()
        return jsonify(data)
    elif kind == "historical":
        # TODO
        data = {}
        return  jsonify(data)
    else:
        return _not_found()

    


# 404 - NOT FOUND
@api.errorhandler(404)
def _not_found(msg="😭 File not found!"):
    message = {"status": 404, "message": str(msg)}
    resp = jsonify(message)
    resp.status_code = 404

    return resp


# 405 - METHOD_NOT_ALLOWED
@api.errorhandler(405)
def _method_not_allowed(msg="This method is not supported for this request !"):
    return jsonify({"status": 405, "message": msg}), 405


# 500 - INTERNAL_SERVER_ERROR
@api.errorhandler(500)
def _internal_server_error(
    msg="Something, somewhere, has gone sideways.\nSo basically, shit happens..."
):
    return jsonify({"status": 500, "message": str(msg)}), 500


# The default_error_handler  will not return any response
# if the Flask application  is running in DEBUG mode.
@api.errorhandler
def default_error_handler(err):
    msg = "An unhandled exception occurred. ==> {}".format(str(err))
    # logger.error(msg)

    # if not settings.FLASK_DEBUG:
    return jsonify({"status": 500, "message": msg}), 500


def _configure_api_doc():
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


def configure_api():
    # Compress each response which content-length > 600
    Compress(api)

    # Enable CORS headers on each api routes
    CORS(api, allow_headers="Content-Type")

    _configure_api_doc()

    return api


if __name__ == "__main__":
    configure_api()
    api.run(debug=False, host="0.0.0.0")
