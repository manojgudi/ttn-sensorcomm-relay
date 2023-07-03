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
    The route to recieve the data from TTN and relay it to the sensor.community

    # NOTE
    Ideally we should be sending 1 request per sensor module, but there's a bug
    in the sensor.community and hence we have to send all the payload in a single REST API
    The dashboard DOESNT distinguish SDS & BME as two different sensors
    """
    fromGW = request.get_json(force=True)
    print(fromGW)
    if "data" in fromGW:
        payload = base64.b64decode(fromGW["data"])

 	# Relay the SDS data to sensor.community
    headers = {"X-Pin":"1", "X-Sensor" : sensorUID, "Content-Type" : "application/json"}
    requestBody = fromGW["uplink_message"]["decoded_payload"]
    url = "https://api.sensor.community/v1//push-sensor-data/"
    sensorCommunityResponse = requests.post(url, json = requestBody, headers = headers)

    # TODO When the API bug is resolved Relay the BME280 data to sensor.community
    """
    headers = {"X-Pin":"11", "X-Sensor" : sensorUID, "Content-Type" : "application/json"}
    requestBody = fromGW["uplink_message"]["decoded_payload"]
    url = "https://api.sensor.community/v1//push-sensor-data/"
    sensorCommunityResponse2 = requests.post(url, json = requestBody, headers = headers)
    """

    # If you get HTTP 2XX then move on
    if (int(sensorCommunityResponse.status_code/100) == 2):
        return make_response("Successfully sent data to sensor-community", 200)

    return make_response("Failed :" + sensorCommunityResponse.text, 501)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--http_port',  default=9999,
                        help="set http port for POST requests")

    args = parser.parse_args()
    defPort = args.http_port

    app.run(host="0.0.0.0", port=defPort)

