import network
import time
from time import sleep

""" Classe per gestire la connessione alla Wifi """
class WiFi:
    """ Costruttore """
    def __init__(self, hotspot, password):
        self.sta_if = network.WLAN(network.STA_IF) 
        self.hotspot=hotspot
        self.password=password
        
        
    """ Effettua la connessione alla wifi """
    def connectionWiFi(self):
        if not self.sta_if.isconnected():
            self.sta_if.active(True)
        x = 0.1
        timeout = 3
        try:
            self.sta_if.connect(self.hotspot, self.password)
            while not self.sta_if.isconnected() and timeout>0:
                sleep(x)
                timeout = timeout - x
         except OSError as e:
            self.disconnectWiFi()


    """ Controlla se c'è connessione """   
    def isconnected(self):
        return self.sta_if.isconnected()
        
        
    """ Effettua la disconnessine """
    def disconnectWiFi(self):
        self.sta_if.disconnect()
        self.sta_if.active(False)
        
    
        
        



