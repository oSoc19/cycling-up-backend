from flask import Flask
from flask import request, make_response, jsonify
import api.getters as getters

app = Flask(__name__)

@app.route('/')
@app.route('/ping')
@app.route('/api/ping')
def api_ping():
    return jsonify(message="Yello World !")



# annotation specifies route
@app.route("/api/map/historical")
def getMapHistorical():
    # extract argument from request
    date = request.args.get('date')
    return getters.getMatchedFeaturesHistorical(date)

if __name__ == "__main__":
    app.run(debug=True)
