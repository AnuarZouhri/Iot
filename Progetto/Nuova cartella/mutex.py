from machine import Pin, PWM
from time import sleep
import Led


class Mutex():
    
    def __init__(self, pin1, pin2, pin3):
        self.red=Led(pin1)
        self.green=Led(pin2)
        self.yellow=Led(pin3)
        self.alarmActivated=False
    
    ''' La porta è chiusa quindi solo il led rosso è acceso'''
    def lock(self):
        self.alarmActivated=False
        self.green.ledOff()
        self.yellow.ledOff()
        self.red.ledOn()
    
    ''' La porta è aperta quindi solo il led verde è acceso'''
    def unlock(self):
        self.alarmActivated=False ''' quando l'allarme viene sbloccato, la porta si chiude? '''
        self.red.ledOff()
        self.yellow.ledOff()
        self.green.ledOn()
    
    ''' Si attiva l'allarme quindi il led giallo lampeggia'''
    def alarm(self):
        self.red.ledOff()
        self.green.ledOff()
        self.alarmActivated=True
        while self.alarmActivated:
            self.yellow.ledOn()
            sleep(0.5)
    
    ''' L'allarme viene sbloccato '''
    def alarmUnlocked(self):
        self.alarmActivated=False
        
        