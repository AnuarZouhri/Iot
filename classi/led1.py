from machine import Pin

""" Classe per l'oggetto Led """
class Led:
    
    """ Costruttore """
    def __init__(self, pin):
        
        """ Inizializzazione dell'oggetto Pin """
        self.led = Pin(pin, Pin.OUT)
        
    """ Metodo per l'accensione del led """
    def ledOn(self):
        self.led.on()
    
    """ Metodo per lo spegnimento del led """
    def lefOff(self):
        self.led.off()
