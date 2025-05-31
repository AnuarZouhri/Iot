from dht22 import DHT22
from UltrasonicSensor import HCSR04

class SensorHandler:
    
    def __init__(self,dht22,hcsr04):
        
        self.dht22 = dht22
        self.hcsr04 = hcsr04
        
    
    def read(self):
        dht_values = self.dht22.measure()
        hcsr04_values = self.hcsr04.distanceCm()
        #joystick_values = self.joystick.readY()
        
        dict_values = { "Temperature": dht_values[0] ,
                        "Humidity": dht_values[1],
                        "Distance cm" : hcsr04_values
                      }
        return dict_values
    
