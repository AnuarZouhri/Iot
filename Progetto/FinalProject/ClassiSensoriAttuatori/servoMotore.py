from machine import Pin, PWM
from time import sleep

""" Classe per gestire il servo motore """
class ServoMotor():
    
    """ Costruttore"""
    def __init__(self,sig_pin,freq=50):
        self.pwm=PWM(sig_pin,freq)
    
    """ Imposta l'angolo di rotazione del servo motore """
    def set_angle(self,angle):
        self.duty_min = 35
        self.duty_max = 133
        self.pwm.duty(int(self.duty_min + (angle/180)*(self.duty_max-self.duty_min)))
        
    """ Imposta l'angolo di rotazione a 0 """
    def openDoor(self, angle=0):
        self.set_angle(angle)
        
    """ Imposta l'angolo di rotazione a 90 """
    def closeDoor(self, angle=90):
        self.set_angle(angle)
        



