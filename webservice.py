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
apiKEY    = os.environ.get("MODULE_API_KEY")
if not sensorUID:
	raise Exception("Please export your SENSOR_UID value from sensor.community!")

if not apiKEY:
	raise Exception("Please export your MODULE_API_KEY value which is written into the module!")


@app.route('/')
def hello():
    return "Hello, World!"

@app.route("/module/", methods=['POST'])
def relayDataFromModule():
    """
    This route is to receive the data from the module directly and relay it to the sensor.community 
    """
    fromModule = request.get_json(force=True)
    print("Request Payload", fromModule)

    if "data" in fromGW:
        payload = base64.b64decode(fromGW["data"])

    # API Key check
    if fromModule["api_key"] != apiKey:
        return make_response("Failed : Invalid API Key "+fromModule["api_key"], 501)

    # Forward it to the /lns/ route internally
    jsonData = {"uplink_message" : {"decoded_payload" : { "sensordatavalues" : fromModule["sensordatavalues"], "software_version" : "test-imt-v0.2"  }}}
    internalURL = request.host_url + url_for('relayDataFromLNS')
    response = requests.post(internalURL, json=jsonData)

    if response.status_code == 200:
        return make_response("Successfully sent data to sensor-community", 200)

    return make_response("Failed : Internal request "+ response.text, 501)
\

@app.route('/lns/', methods=['POST'])
def relayDataFromLNS():
    """
    The route is to recieve the data from TTN and relay it to the sensor.community

    # NOTE
    Ideally we should be sending 1 request per sensor module, but there's a bug
    in the sensor.community and hence we have to send all the payload in a single REST API
    The dashboard DOESNT distinguish SDS & BME as two different sensors
    """
    fromGW = request.get_json(force=True)
    print("Request Payload", fromGW)
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

