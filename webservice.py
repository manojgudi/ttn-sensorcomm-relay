import argparse
import base64
import os
import pprint
import requests

from flask import request
from flask import Flask, jsonify, make_response

app = Flask(__name__)

# Get sensor value required for relaying data to sensor.community
sensorUID = os.environ.get("SENSOR_UID")
if not sensorUID:
	raise Exception("Please export your SENSOR_UID value from sensor.community!")

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/api/data')
def get_data():
    data = {'name': 'John Doe', 'age': 30, 'city': 'New York'}
    return jsonify(data)

@app.route('/lns/', methods=['POST'])
def relayDataFromLNS():
    """
    """
    fromGW = request.get_json(force=True)
    print(fromGW)
    if "data" in fromGW:
        payload = base64.b64decode(fromGW["data"])

 	# Relay the data to sensor.community
    headers = {"X-Pin":"1", "X-Sensor" : sensorUID, "Content-Type" : "application/json"}
    requestBody = fromGW["uplink_message"]["decoded_payload"]
    url = "https://api.sensor.community/v1//push-sensor-data/"
    x = requests.post(url, json = requestBody, headers = headers)
    print("Sensor community post-return", x.text)

    return make_response('OK', 200)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--http_port',  default=9999,
                        help="set http port for POST requests")

    args = parser.parse_args()
    defPort = args.http_port

    app.run(host="0.0.0.0", port=defPort)

