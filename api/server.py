from flask import Flask
from flask import request
import getters as getters

app = Flask(__name__)

# annotation specifies route
@app.route("/api/map/historical")
def getMapHistorical():
    # extract argument from request
    date = request.args.get('date')
    return getters.getMatchedFeaturesHistorical(date)

if __name__ == "__main__":
    app.run(debug=True)
