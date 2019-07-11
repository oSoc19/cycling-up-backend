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
@app.route("/api/map/historical/<year>")
def getMapHistorical(year):
    # extract argument from request
    return jsonify(getters.getMatchedFeaturesHistorical(year))

### general map ###
@app.route("/api/map/general/<kind>")
def getMapBicyclePump(kind):
    data = getters.getJsonContents(kind)
    if data is not None:
        return jsonify(data)
    else:
        return not_found()


# file not found error
@app.errorhandler(404)
def not_found():
    message = {
        'status': 404,
        'message': 'File not found!'
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp



def configure_app():
    return app

if __name__ == "__main__":
    configure_app()
    app.run(debug=True)
