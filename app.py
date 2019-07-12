from flask import Flask
from flask import request, make_response, jsonify
from flask_compress import Compress
from flask_cors import CORS

import api.getters as getters


api = Flask(__name__)

# Compress each response which content-length > 600
Compress(api)

# Enable CORS headers on each api routes
CORS(api, allow_headers="Content-Type")


@api.route("/")
@api.route("/api/ping")
def api_ping():
    """
    Route to check the connectivity
    """
    return jsonify(message="Yello World !")


### GET historical infra map ###
@api.route("/api/map/historical/<int:year>")
def getMapHistorical(year):
    return jsonify(getters.getMatchedFeaturesHistorical(year))


### GET general map ###
@api.route("/api/map/general/<string:kind>")
def getGeneralMap(kind):
    data = getters.getJsonContents(kind)
    if data is not None:
        return jsonify(data)
    else:
        return _not_found()


# 404 - NOT FOUND
@api.errorhandler(404)
def _not_found(msg="😭 File not found!"):
    message = {"status": 404, "message": msg}
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
    return jsonify({"status": 500, "message": msg}), 500


# The default_error_handler  will not return any response
# if the Flask application  is running in DEBUG mode.
@api.errorhandler
def default_error_handler(err):
    msg = "An unhandled exception occurred. ==> {}".format(str(err))
    # logger.error(msg)

    # if not settings.FLASK_DEBUG:
    return jsonify({"status": 500, "message": msg}), 500


def configure_api():
    return api


if __name__ == "__main__":
    configure_api()
    api.run(debug=True, host="0.0.0.0")
