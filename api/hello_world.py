from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/api/")
def hello():
    kind = request.args.get('kind')
    date = request.args.get('date')
    return "Hello world!" + kind + date
