"""


"""

## Dependency

# Standard

# Third party
from flask import Flask, request, make_response, jsonify, abort
from flasgger import swag_from

# Local
import api.getters as getters


def configure_routes(api: Flask, config: dict) -> None:
    """[summary]

    Arguments:
        api {Flask} -- [description]
        config {Config} -- [description]

    Returns:
        None -- [description]
    """

    @api.route("/")
    @api.route("/api/ping")
    @swag_from("swagger/get_ping.yml")
    def api_ping():
        """
        Route to check the connectivity
        """
        return jsonify(message="Yello World !")

    @api.route("/api/map/historical/<int:year>")
    @swag_from("swagger/get_map_historical.yml")
    def getMapHistorical(year: int):
        """
        Get the historical map

        Arguments:
            year {int} -- The required year
        """

        return jsonify(getters.getMatchedFeaturesHistorical(year))

    @api.route("/api/map/general/<string:kind>")
    @swag_from("swagger/get_map_general.yml")
    def getGeneralMap(kind: str):
        """
        Retrieve the general map

        Arguments:
            kind {string} -- The required kind of map
        """

        data = getters.getJsonContents(kind)
        if data is not None:
            return jsonify(data)
        else:
            return abort(404)

