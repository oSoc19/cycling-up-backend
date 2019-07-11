from flask import Flask
from flask import request, make_response, jsonify
from flask_compress import Compress


import api.getters as getters


app = Flask(__name__)
Compress(app)


@app.route('/')
@app.route('/ping')
@app.route('/api/ping')
def api_ping():
    """
    Route to check the connectivity
    """
    return jsonify(message="Yello World !")



# annotation specifies route
@app.route("/api/map/historical")
def getMapHistorical():
    # extract argument from request
    date = request.args.get('date')
    return jsonify(data=getters.getMatchedFeaturesHistorical(date))


def configure_app():
    return app


if __name__ == "__main__":
    configure_app()
    app.run(debug=True)
