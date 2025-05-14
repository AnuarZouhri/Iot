from machine import Pin, I2C
import ssd1306
import framebuf
import network
import time
from time import sleep, ticks_ms, ticks_diff
import dht
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

sensor = dht.DHT22(Pin(15))

#risoluzione del display OLED: 128x64 pixel
WIDTH = 128
HEIGHT = 64
SCL_PIN = 22
SDA_PIN = 21



i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
button = Pin(4,Pin.IN,Pin.PULL_DOWN)

display.fill(0)
last_click = 0 #utilizziamo questa variabile per misurare la durata del rimbalzo
button_message = "0"

def switch(pin): 
    global last_click, button_message
    print('button pressed')
    current_click = ticks_ms()
    delta = ticks_diff(current_click,last_click)
    if delta < 50 :
        return
    last_click = current_click
    if button_message == "0":
        button_message = "1"
    else:
        button_message = "0"
        
def connectionWifi():
    display.fill_rect(0,0,128,64,0)
    display.text("Connecting to",1,1,1)
    display.text("Wifi",1,10,1)
    display.show()
    print("Connecting to WiFi", end="")
    
    sta_if.active(True)
    sta_if.connect('Galaxy A5173BB', 'aaaaaaab')
    points = 0
    while not sta_if.isconnected():
      
      if(points == 3):
          display.fill_rect(30,10,20,8,0)
       
          display.show()
      display.text('.',30+3*points,10,1)
      display.show()
      points = points + 1
      print(".", end="")
      time.sleep(0.3)
    display.show()
    display.text("Connected",1,20,1)
    display.show()
    print(" Connected!")


def connectionClient():        
    display.text("Connecting to",1,30,1)
    display.text("MQTT server...",1,40,1)
    display.show()
    print("Connecting to MQTT server... ", end="")
    client.connect()
    client.set_callback(sub_callback_handler)
    client.subscribe(MQTT_TOPIC_SUB1)
    client.subscribe(MQTT_TOPIC_SUB2)
    display.text("Connected",1,50,1)
    display.show()
    print("Connected!")
    
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

       #elif sta_if.iconnected() == False and msg == 0:
         #   sta_if.connect('Galaxy A5173BB', 'aaaaaaab')

sta_if = network.WLAN(network.STA_IF)
connectionWifi()
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD,keepalive=60)
connectionClient()

prev_weather = ""
prev_button = ""


button.irq(handler=switch, trigger=Pin.IRQ_RISING)

while True:
  client.check_msg()
  print("Measuring temperature and humidity... ", end="")
  sensor.measure() 
  message = ujson.dumps({
    "temp": sensor.temperature(),
    "humidity": sensor.humidity(),
  })
  if message != prev_weather:
    print("Updated!")
    #print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
    client.publish(MQTT_TOPIC_SUB1, message)
    prev_weather = message
  else:
    print("No change")
  time.sleep(1)
  '''if button_message != prev_button:
      print('invio',button_message)
      client.publish(MQTT_TOPIC_SUB2, button_message)
      prev_button = button_message
      print(prev_button)
'''

button.irq(handler=switch, trigger=Pin.IRQ_RISING)



