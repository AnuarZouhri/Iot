from machine import Pin, PWM
from time import sleep, sleep_ms
from LedPwm import LEDPwm
from Led import LED


""" Classe per gestire il semaforo """
class Mutex():
    
    """ Costruttore """
    def __init__(self, pin1, pin2, pin3):
        self.red=LED(pin1)
        self.red.ledOff()
        self.green=LED(pin2)
        self.green.ledOff()
        self.yellow=LEDPwm(pin3, 5000, 0)
        self.yellow.setDuty(0)
    
    """ Attiva solo il led rosso """
    def lock(self):
        self.green.ledOff()
        self.yellow.setDuty(0)
        self.red.ledOn()
    
    """ Attiva solo il led verde """
    def unlock(self):
        self.red.ledOff()
        self.yellow.setDuty(0)
        self.green.ledOn()
    
    """ Attiva solo il led giallo il quale lampeggia """
    def alarm(self):
        self.red.ledOff()
        self.green.ledOff()
        for duty in range(0,1024, 5): 
            self.yellow.setDuty(duty)
            sleep_ms(5)
        for duty in range(1023,-1, -5):
            self.yellow.setDuty(duty)
            sleep_ms(5)
     
        

        
        
        
        



