from dht22 import DHT22

""" Classe create per ottenere i valori letti dal sensore di umidità e temperatura """
class SensorHandler:
    
    """ Costruttore """
    def __init__(self,dht22):
        self.dht22 = dht22
        
        
    """ Legge i valori e ne crea un dizionario """
    def read(self):
        dht_values = self.dht22.measure()
        dict_values = { "Temperature": dht_values[0] ,
                        "Humidity": dht_values[1]
                      }
        return dict_values
    
