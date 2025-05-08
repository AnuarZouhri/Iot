from machine import Pin, PWM
import Led


class Mutex():
    
    def __init__(self, pin1, pin2, pin3):
        self.red=LED(pin1)
        self.green=LED(pin2)
        self.yellow=LED(pin3, False)
        
    def lock(self):
        self.green.ledOff()
        self.yellow.ledDuty(0)
        self.red.ledOn()
        
    def unlock(self):
        self.red.ledOff()
        self.yellow.ledDuty(0)
        self.green.ledOn()
        
    def alarm(self):
        self.red.ledOff()
        self.green.ledOff()
        self.yellow.ledDuty(50)
        
        