from flask import Flask
from flask import request, make_response, jsonify
from flask_compress import Compress
from flask_cors import CORS

import api.getters as getters


app = Flask(__name__)

# Compress each response which content-length > 600
Compress(app)

# Enable CORS headers on each api routes
CORS(app, allow_headers='Content-Type')


@app.route('/')
@app.route('/ping')
@app.route('/api/ping')
def api_ping():
    """
    Route to check the connectivity
    """
    return jsonify(message="Yello World !")



### historical infra map ###
@app.route("/api/map/historical")
def getMapHistorical():
    # extract argument from request
    date = request.args.get('date')
    return jsonify(getters.getMatchedFeaturesHistorical(date))

### general map ###
@app.route("/api/map/general/bike_pump")
def getMapBicyclePump():
    return jsonify(getters.getJsonContents('process_data/data/bike_pump.json'))

@app.route("/api/map/general/bike_parking")
def getMapBikeParking():
    return jsonify(getters.getJsonContents('process_data/data/bike_parking.json'))

@app.route("/api/map/general/bike_shop")
def getMapBikeShop():
    return jsonify(getters.getJsonContents('process_data/data/bike_shop.json'))



def configure_app():
    return app

if __name__ == "__main__":
    configure_app()
    app.run(debug=True)
