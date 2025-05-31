from dht22 import DHT22
import os

""" Classe create per ottenere i valori letti dal sensore di umidità e temperatura """
class SensorHandler:
    
    """ Costruttore """
    def __init__(self,dht22, hcsr04, sogliaTemp=50.0, sogliaHum=70.0, sogliaDis=10.0):
        self.dht22 = dht22
        self.hcsr04 = hcsr04
        self.sogliaTemp = ''
        self.sogliaHum = ''
        self.sogliaDis = ''
        
        if 'temp.txt' in os.listdir():
            with open('temp.txt', 'r') as f:
                self.sogliaTemp = f.read()
        else:
            with open('temp.txt', 'w') as f:
                f.write(str(sogliaTemp))
         
        if 'hum.txt' in os.listdir():
            with open('hum.txt', 'r') as f:
                self.sogliaHum = f.read()
        else:
            with open('hum.txt', 'w') as f:
                f.write(str(sogliaHum))
                
        if 'dis.txt' in os.listdir():
            with open('dis.txt', 'r') as f:
                self.sogliaDis = f.read()
        else:
            with open('dis.txt', 'w') as f:
                f.write(str(sogliaDis))
        
        self.sogliaTemp = float(self.sogliaTemp)
        self.sogliaHum = float(self.sogliaHum)
        self.sogliaDis = float(self.sogliaDis)
        
        
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
        with open('temp.txt', 'w') as f:
            f.write(str(sogliaTemp))
        
    def setSogliaHum(self, sogliaHum):
        self.sogliaHum = sogliaHum
        with open('hum.txt', 'w') as f:
            f.write(str(sogliaHum))
        
    def setSogliaDis(self, sogliaDis):
        self.sogliaDist = sogliaDist
        with open('dis.txt', 'w') as f:
            f.write(str(sogliaDis))
        
        
    def getSogliaTemp(self):
        return self.sogliaTemp
    
    def getSogliaHum(self):
        return self.sogliaHum

    def getSogliaDis(self):
        return self.sogliaDis
