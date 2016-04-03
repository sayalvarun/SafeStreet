import json
from flask import Flask, render_template,Response,make_response,request
import directions
import os

project_root = os.path.dirname(__file__)
app = Flask(__name__, template_folder=project_root)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getCoordinates", methods=['GET','POST'])
def getCoords():
    source = request.args.get('source')
    dest = request.args.get('destination')
    points = directions.computeNewWaypoints(directions.getDirectionPoints(source,dest))
    result = directions.getWaypoints(points,source,dest)
    return json.dumps(result)

if __name__ == '__main__':
    app.run()
