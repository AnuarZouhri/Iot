from machine import Pin
import dht

class DHT:
    
    def __init__(self,Pin_In):
        self.sensor = dht.DHT22(Pin(15))
        
    def measure(self):
        self.sensor.measure()
        return [self.sensor.temperature(),self.sensor.humidity()]

        