# TTN to Sensor Community Relay Webservice

A simple python flask webservice which listens to data from TTN (The Things Network) for LoRa messages and relays it to sensor.community.

We are using this service to push the SDS011 and BME 280 data from our LoRa device to sensor.community.


## How to deploy


First we obtain the sensor ID assigned to us after we register our device on sensor.community. We must export it, for instance, we can put this in our bashrc

```sh
$ echo "export SENSOR_ID="esp8266-MySensorID"
```

Since the built-in debug server of flask is good enough for this simple application, we can simply deploy it as:

```sh
$ nohup python3 webservice.py --http_port=12001 &
```
