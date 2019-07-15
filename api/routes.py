#!/usr/bin/env python3

from flask import Flask
from flask import request, make_response, jsonify
from flask_compress import Compress
from flask_cors import CORS
from flasgger import Swagger, swag_from

import api.getters as getters


def configure_api_routes(api:Flask, config) -> None:

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

