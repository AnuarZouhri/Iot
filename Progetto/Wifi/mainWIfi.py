import machine
from wificlass import WiFi
from OledClass import Oled
from time import sleep

wf=WiFi('Galaxy A5173BB', 'aaaaaaab')
oled = Oled()

was_connected = 0
b = 0
a =0
while True:
    
    if b==1:
        a = int(input('Inserisci un numero'))
        b = b-1
    
    if a == 1:
        oled.write(1,20,0,'Connecting to\nWiFi')
        oled.show()
        sleep(1)
        wf.connectionWiFi()
        oled.write(1,20,0,'Connected to\nWiFi')
        oled.show()
        was_connected = 1
    
    oled.write(1,1,0,'Menu')
    oled.show()
    sleep(5)
    a=0
    
    
    if not wf.isconnected():
        #print('non connesso')
        l=oled.write(1,1,0,'Lost Connection!')
        oled.show()
        sleep(2)
        was_connected = 0
        

    
        
    