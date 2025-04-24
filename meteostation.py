import os
from pathlib import Path

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

import bme
import mh_z19

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

MQTT_IP = os.getenv("MQTT_IP")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_PORT = 1883
MQTT_TOPIC = 'home/sensors/bme280'


client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_IP, MQTT_PORT, 60)

temperature, pressure, humidity = bme.readBME280All()
co2_ppm = mh_z19.get_sensor_data()

payload = f'{{"temperature": {temperature:.2f}, "humidity": {humidity:.2f}, "pressure": {pressure:.2f}, "co2": {co2_ppm}}}'
client.publish(MQTT_TOPIC, payload)
print(f"Published: {payload}")
