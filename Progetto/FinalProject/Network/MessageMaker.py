import ujson

""" Classe per gestire i messaggi da pubblicare tramite MQTT """
class MM:
    
    """ Costruttore """
    def __init__(self):
        self.prevTemp     = ''
        self.prevHum      = ''
        self.prevDistance = ''
        
        
    """ Invia un messaggio contenente lo stato della temperatura """
    def temperatureMsg(self,temp):
        tempMsg = ujson.dumps({"temp": temp,})
        
        if tempMsg != self.prevTemp:
            self.prevTemp= tempMsg
            return tempMsg
        else: return None
        
        
    """ Invia un messaggio contenente lo stato dell'umidità"""
    def humidityMsg(self,hum):
        humMsg = ujson.dumps({"humidity": hum,})
        
        if humMsg != self.prevHum:
            self.prevHum= humMsg
            return humMsg
        else: return None


    """ Invia un messaggio contenente 1 """
    def correctPinMsg(self):
        return ujson.dumps({"correct": 1,})
    
    
    """ Invia un messaggio contenente 0 """
    def wrongPinMsg(self):
        return ujson.dumps({"wrong": 0,})
    
    
    """ Invia un messaggio contenente lo stato della porta: 2 se è chiusa, 3 se è aperta """
    def statusDoor(self, x):
        if x==0:
            return ujson.dumps({"wrong": 2,})
        elif x==1:
            return ujson.dumps({"correct": 3,})
    
         