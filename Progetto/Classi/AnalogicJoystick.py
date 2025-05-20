from machine import Pin, ADC
import time
from time import sleep



class AnalogicJoystick:
    def __init__(self, pinY, pinSW):
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
        #val = val * (3.3 / 4095)
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
    Restituisce
    -1 se il joystick è al centro
    0 se il joystick è andato verso il basso quindi la porta deve chiudersi
    1 se il joystick è andato veros l'alto quindi la prota deve aprirsi
    '''
    def goUp(self):
        val=self.readY()
        print(val)
        if val<2700:
            return 1
        elif val>2850:
            return 0
        else:
            return -1	
        

        
'''
aj=AnalogicJoystick(26,4,14)


while True:
    print(aj.goUp())
    sleep(1)
'''


