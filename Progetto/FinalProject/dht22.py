from machine import Pin
from time import sleep
import dht


"""
    Classe per il sensore di temperatura e umidità.
"""
class DHT22:
    
    
    """
        Il costruttore riceve un pin come parametro e lo utilizza per inizializzare
        l'oggetto di classe DHT22 appartenente alla libreria dht.
    """
    def __init__(self, Pin_In):
        self.sensor = dht.DHT22(Pin(Pin_In))
        
        
    """
        Il metodo measure() esegue il metodo measure() della classe DHT22 della libreria dht
    """
    def measure(self):
        try:
            self.sensor.measure()
            return [self.sensor.temperature(), self.sensor.humidity()]
        except OSError as e:
            print("Errore lettura DHT22:", e)
            return [None, None]           