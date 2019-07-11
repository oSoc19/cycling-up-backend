from flask import Flask
from flask import request, make_response, jsonify
import api.getters as getters

app = Flask(__name__)

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



if __name__ == "__main__":
    app.run(debug=True)
