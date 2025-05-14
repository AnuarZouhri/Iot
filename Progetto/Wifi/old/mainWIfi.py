import machine
from wificlass import WiFi

wf=WiFi('Galaxy A5173BB', 'aaaaaaab')

while True:
    if not wf.isconnected():
        print('non connessooooo')
        wf.connectionWifi()
    else:                                                                
        print('connessoooo')