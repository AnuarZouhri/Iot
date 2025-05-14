#import wifi
import framebuf
import network
import time
from time import sleep
import ujson
from umqtt.simple import MQTTClient

# MQTT Server Parameters

MQTT_CLIENT_ID = "micropython-dht12-demo"
MQTT_BROKER    = "broker.hivemq.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = b'wokwi'
MQTT_TOPIC_SUB1 = b'wokwi/Oled'
MQTT_TOPIC_SUB2 = b'wokwi/Button'

print("Connecting to MQTT server... ", end="")
client.connect()
client.set_callback(sub_callback_handler)
client.subscribe(MQTT_TOPIC_SUB1)
client.subscribe(MQTT_TOPIC_SUB2)
print("Connecting to MQTT server... ", end="")
client.connect()
client.set_callback(sub_callback_handler)
client.subscribe(MQTT_TOPIC_SUB1)
client.subscribe(MQTT_TOPIC_SUB2)

while True: