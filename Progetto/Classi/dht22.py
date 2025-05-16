from machine import Pin
import dht

class DHT22:
    
    def __init__(self,Pin_In):
        self.sensor = dht.DHT22(Pin(Pin_In))
        
    def measure(self):
        self.sensor.measure()
        return [self.sensor.temperature(),self.sensor.humidity()]

        