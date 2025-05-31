from dht22 import DHT22

""" Classe create per ottenere i valori letti dal sensore di umidità e temperatura """
class SensorHandler:
    
    """ Costruttore """
    def __init__(self,dht22, hcsr04, sogliaTemp=50, sogliaHum=70, sogliaDis=10):
        self.dht22 = dht22
        self.hcsr04 = hcsr04
        self.sogliaTemp = sogliaTemp
        self.sogliaHum = sogliaHum
        self.sogliaDis = sogliaDis
        
        
    """ Legge i valori e ne crea un dizionario """
    def readDht22(self):
        dht_values = self.dht22.measure()
        dict_values = { "Temperature": dht_values[0] ,
                        "Humidity": dht_values[1]
                      }
        return dict_values
    
    
    def readHcsr04(self):
        return self.hcsr04.distanceCm()
    
    
    def checkDistance(self):
        return self.readHcsr04() < self.sogliaDis
    
    
    def checkTempHum(self, temp, hum):
        if temp is not None and temp >= self.sogliaTemp:
            return 1
        elif hum is not None and hum >= self.sogliaHum:
            return 2
        
        return 0
        
    def setSogliaTemp(self, sogliaTemp):
        self.sogliaTemp = sogliaTemp
        
    def setSogliaHum(self, sogliaHum):
        self.sogliaHum = sogliaHum
        
    def setSogliaDis(self, sogliaDis):
        self.sogliaDist = sogliaDist
        
        
    def getSogliaTemp(self):
        return self.sogliaTemp
    
    def getSogliaHum(self):
        return self.sogliaHum

    def getSogliaDis(self):
        return self.sogliaDis
