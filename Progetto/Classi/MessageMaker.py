import ujson

class MM:
    
    def __init__(self):
        self.prevTemp     = ''
        self.prevHum      = ''
        self.prevDistance = ''
        
    
    def temperatureMsg(self,temp):
        tempMsg = ujson.dumps({
        "temp": temp,
        })
        
        if tempMsg != self.prevTemp:
            self.prevTemp= tempMsg
            return tempMsg
        else: return None
        
    def humidityMsg(self,hum):
        humMsg = ujson.dumps({
            "humidity": hum,
        })
        
        if humMsg != self.prevHum:
            self.prevHum= humMsg
            return humMsg
        else: return None
        
    def disMessage(self,dis):
        disMsg = ujson.dumps({
        "distance": dis,
        })
        
        if disMsg != self.prevDistance:
            self.prevDistance = disMsg
            return disMsg
        else: return None
      
    def correctPinMsg(self):
        return ujson.dumps({
        "correct": 1,
        })
    
    def wrongPinMsg(self):
        return ujson.dumps({
        "wrong": 0,
        })
    
         