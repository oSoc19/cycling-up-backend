from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/api/map/historical")
def hello():
    kind = request.args.get('kind')
    date = request.args.get('date')
    
    with open('match_dates/bike_infra.geojson', 'r') as sourceDate:
        



if __name__ == "__main__":
    app.run(debug=True)
