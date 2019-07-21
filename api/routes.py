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

    @api.route("/ping")
    @swag_from("swagger/get_ping.yml")
    def api_ping():
        """
        Route to check the connectivity
        """
        return jsonify(message="Yello World !")


    @api.route("/map/historical/years")
    @swag_from("swagger/get_map_historical years.yml")
    def getMapHistoricalYears():
        """
        Get the available historical year
        """
        return jsonify(getters.getHistoricalYears())


    @api.route("/map/historical/<int:year>")
    @swag_from("swagger/get_map_historical.yml")
    def getMapHistorical(year: int):
        """
        Get the historical map

        Arguments:
            year {int} -- The required year
        """

        return jsonify(getters.getMatchedFeaturesHistorical(year))

    @api.route("/map/general/<string:kind>")
    @swag_from("swagger/get_map_general.yml")
    def getGeneralMap(kind: str):
        """
        Retrieve the general map

        Arguments:
            kind {string} -- The required kind of map
        """

        data = getters.getFetchedMobigisJsonContents(kind)
        if data is not None:
            return jsonify(data)
        else:
            return abort(404)

    @api.route("/bike_count/stations")
    @swag_from("swagger/get_bike_count_stations.yml")
    def getBikeCountStations():
        """
        Retrieve the bike count stations.
        """

        data = getters.getHistoricalJsonContents('historic_bike_stations')

        if data is not None:
            return jsonify(data)
        else:
            return abort(404)

    @api.route("/bike_count/<int:id>")
    @swag_from("swagger/get_bike_count_data.yml")
    def getBikeCountData(id: int):
        """
        Retrieve the bike count data, for the counting location corresponding to the given id.

        Arguments:
            id {int} -- The requested counting location
        """

        data = getters.getBikeCountData(id)
        if data is not None:
            return jsonify(data)
        else:
            return abort(404)

    # Historic data
    @api.route("/historical/<string:kind>")
    @swag_from("swagger/get_historical_data.yml")
    def getHistoricalData(kind: str):
        """
        Retrieve the required villo data, with kind the name of the json file.
        """
        data = getters.getHistoricalJsonContents(kind)

        if data is not None:
            return jsonify(data)
        else:
            return abort(404)
