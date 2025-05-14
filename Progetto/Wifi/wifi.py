from wificlass import WiFi
import framebuf
import network
import time
from time import sleep
import ujson
from mqttclass import MQTT

# MQTT Server Parameters

MQTT_CLIENT_ID = "micropython-dht12-demo"
MQTT_BROKER    = "broker.hivemq.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = b'wokwi'
MQTT_TOPIC_SUB1 = b'wokwi/Oled'
MQTT_TOPIC_SUB2 = b'wokwi/Button'

def sub_callback_handler(topic,msg):
    
        if topic == MQTT_TOPIC_SUB1:
            data = ujson.loads(msg)
            temp = data["temp"]
            hum = data["humidity"]
            display.fill_rect(0,0,128,64,0)        
            display.text("Temp: "+str(temp), 9, 1, 1)
            display.text("Hum: "+str(hum), 9, 11, 1)   
            display.show()
            
        if topic == MQTT_TOPIC_SUB2:
            if sta_if.isconnected() ==False and msg.decode() == "0":
                print('connetto')
                connectionWifi()   
                connectionClient()

sta_if = WiFi()
sta_if.connectionWifi()
mqtt = MQTT(broker="broker.hivemq.com",client_id="micropython-dht12-demo",user = "",
            password="",topic=b'wokwi',topic_sub=b'wokwi/Oled')
mqtt.connectClient()
'''print("Connecting to WiFi", end="")

sta_if.active(True)
sta_if.connect('Galaxy A5173BB', 'aaaaaaab')
points = 0
while not sta_if.isconnected():
  
  print(".", end="")
  time.sleep(0.3)
print(" Connected!")'''


#print("Connecting to MQTT server... ", end="")


while True:
    if not connection:
        connection()
    print('connect')
