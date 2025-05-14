import framebuf
import network
import time
from time import sleep
import dht
import ujson
from umqtt.simple import MQTTClient

def connectionWifi():
    print("Connecting to WiFi", end="")
    
    sta_if.active(True)
    sta_if.connect('Galaxy A5173BB', 'aaaaaaab')
    points = 0
    while not sta_if.isconnected():
      print(".", end="")
      time.sleep(0.3)

    print(" Connected!")


