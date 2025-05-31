from dht22 import DHT22

""" Classe create per ottenere i valori letti dal sensore di umidità e temperatura """
class SensorHandler:
    
    """ Costruttore """
    def __init__(self,dht22,hcsr04):
        self.dht22 = dht22
        self.hcsr04 = hcsr04
        
        
    """ Legge i valori e ne crea un dizionario """
    def readDht22(self):
        dht_values = self.dht22.measure()
        dict_values = { "Temperature": dht_values[0] ,
                        "Humidity": dht_values[1]
                      }
        return dict_values
    
    
    def readHcsr04(self):
        return self.hcsr04.distanceCm()
    
    
    def checkDistance(self, standardDistance):
        return self.readHcsr04() < standardDistance
    
    
    def checkTempHum(self, temp, tempMax, hum, humMax):
        if temp is not None and temp >= tempMax:
            return 1
        elif hum is not None and hum >= humMax:
            return 2
        
        return 0
        
    
