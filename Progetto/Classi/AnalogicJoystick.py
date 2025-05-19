from machine import Pin, ADC
from time import sleep


class AnalogicJoystick:
    def __init__(self, pinX, pinY, pinSW):
        self.x=ADC(Pin(pinX, Pin.IN))
        self.x.atten(ADC.ATTN_11DB) 
        self.y=ADC(Pin(pinY, Pin.IN))
        self.y.atten(ADC.ATTN_11DB) 
        self.SW=Pin(pinSW, Pin.IN, Pin.PULL_UP)
        self.last_press_time=0
        self.current_time=0
        
    '''
    Restituisce un valore da 0 a 3.3.
    Restituisce 2.20-2.30 se il joystick è al centro
    '''
    def readY(self):
        val=self.y.read()
        val = val * (3.3 / 4095)
        return val
    
    '''
    def readX(self):
        val=self.x.read()
        val = val * (3.3 / 4095)
        return val
    '''
    
    def pressed(self):
        self.current_time = time.ticks_ms()
        if time.ticks_diff(self.current_time, self.last_press_time) < 200:
            return
        self.last_press_time = self.current_time
        
        if self.SW.value()==0:
            return True
        elif self.SW.value()==1:
            return False

        
'''
aj=AnalogicJoystick(26,4,14)
''' 