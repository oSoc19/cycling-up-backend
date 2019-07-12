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
@api.route("/ping")
@api.route("/api/ping")
def api_ping():
    """
    Route to check the connectivity
    """
    return jsonify(message="Yello World !")


### historical infra map ###
@api.route("/api/map/historical/<year>")
def getMapHistorical(year):
    # extract argument from request
    return jsonify(getters.getMatchedFeaturesHistorical(year))


### general map ###
@api.route("/api/map/general/<kind>")
def getGeneralMap(kind):
    data = getters.getJsonContents(kind)
    if data is not None:
        return jsonify(data)
    else:
        return _not_found()


# file not found error
@api.errorhandler(404)
def _not_found(msg="File not found!"):
    message = {"status": 404, "message": msg}
    resp = jsonify(message)
    resp.status_code = 404

    return resp


def configure_api():
    return api


if __name__ == "__main__":
    configure_api()
    api.run(debug=True, host="0.0.0.0")
