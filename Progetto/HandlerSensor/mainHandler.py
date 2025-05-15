from dht22 import DHT22
from AnalogicJoystick import AnalogicJoystick
from UltrasonicSensor import HCSR04
from Handler import SensorHandler
from time import sleep
from wificlass import WiFi
from ServoMotore import ServoMotor

dht22 = DHT22(15)
hcsr04 = HCSR04(5,18)
analogicJ = AnalogicJoystick(26,35,14)
servoM=ServoMotor(4)

wf=WiFi('Galaxy A5173BB', 'aaaaaaab')
handler = SensorHandler(dht22,hcsr04,analogicJ)

was_connected = 0

while True:
    
    '''if not wf.isconnected():
        wf.connectionWiFi()
    
    if wf.isconnected():
        print('connesso')
        sleep(1)
    else:
        print('non connesso')'''
    d = handler.read()
    print(d)
    if d['Y-axis values']>3:
        print('chiudi')
    sleep(1)
    v=0
    servoM.set_angle(0)
    while v!=180:
        print('nel ciclo')
        yaxis=d['Y-axis values']
        print('yaxis',yaxis)
        if yaxis>2.20:
            yaxis=2.20
        v=(yaxis*(-900/11))+180
        print('v',v)
        servoM.openDoor(v)
        d = handler.read()
        sleep(0.3)
    
    
    
    
    
