from machine import Pin, PWM
from time import sleep, sleep_ms
from LedPwm import LedPwm
from Led import Led



class Mutex():
    
    def __init__(self, pin1, pin2, pin3):
        self.red=LED(pin1)
        self.red.ledOff()
        self.green=LED(pin2)
        self.green.ledOff()
        self.yellow=LEDPwm(pin3, 5000, 0)
        self.yellow.setDuty(0)
    
    ''' La porta è chiusa quindi solo il led rosso è acceso'''
    def lock(self):
        self.green.ledOff()
        self.yellow.setDuty(0)
        self.red.ledOn()
    
    ''' La porta è aperta quindi solo il led verde è acceso'''
    def unlock(self):
        self.red.ledOff()
        self.yellow.setDuty(0)
        self.green.ledOn()
    
    ''' Si attiva l'allarme quindi il led giallo lampeggia'''
    def alarm(self):
        self.red.ledOff()
        self.green.ledOff()
        for duty in range(0,1024, 5): 
            self.yellow.setDuty(duty)
            sleep_ms(5)
        for duty in range(1023,-1, -5):
            self.yellow.setDuty(duty)
            sleep_ms(5)
    
        
'''
mt=Mutex(19,4,5)

while True:
    mt.lock()
    sleep(2)
    mt.unlock()
    sleep(2)
    mt.alarm()
    sleep(3)
e'''      
        

        
        
        
        


