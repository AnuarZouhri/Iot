from dht22 import DHT22
from UltrasonicSensor import HCSR04

class SensorHandler:
    
    def __init__(self,dht,hcsr04):
        
        self.dht = dht
        self.hcsr04 = hcsr04
        
    
    def read(self):
        
        dht_values = self.dht.measure()
        hcsr04_values = self.hcsr04.distanceChange()
        
        dict_values = { "Temperaturee": dht_values[0] ,
                        "Humidity": dht_values[1],
                        "Distance change" : hcsr04_values
                      }
        return dict_values