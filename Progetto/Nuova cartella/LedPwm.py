from machine import Pin, PWM

""" Classe per l'oggetto LedPWM """
class LEDPwm:
    
    """ Costruttore """
    def __init__(self, pin, freq, dutyCycle):
        
        """ Inizializzazione del led """
        self.led = PWM(pin, freq)
        self.led.duty(dutyCycle)
    
    """ Setter del duty cycle """
    def setDuty(self, dutyCycle):
        self.led.duty(dutyCycle)
        
    """ Setter della frequency """
    def setFreq(self, freq):
        self.led.freq(freq)
        
    """ Getter del duty cycle """
    def getDuty(self):
        return self.led.duty()
    
    """ Getter della frequency """
    def getFreq(self):
        return self.led.freq()
    
    """ Accensione del led """
    def ledOn(self):
        self.led.on()
        
    """ Spegnimento del led """
    def ledOff(self):
        self.led.off()
    
    
        
    