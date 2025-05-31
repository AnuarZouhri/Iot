import machine
from machine import Pin
from time import sleep_ms


""" Classe per gestire il sensore ad ultrasuoni """
class HCSR04:
    
    """ Costruttore """
    def __init__(self, trigger, echo, timeout=500*2*30):
        self.trigger = Pin(trigger, Pin.OUT)
        self.echo = Pin(echo, Pin.IN)
        self.timeout = timeout
        
    """ Il trigger invia un'onda sonora e si conta per quanti ms echo resta a 1 """
    def pulseAndWait(self):
        self.trigger.value(0)
        sleep_ms(5)
        self.trigger.value(1)
        sleep_ms(100)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.timeout)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110:
                raise OSError('Out of range')
            raise ex

    """ Calcola la distanza in cm tra il sensore ad ultrasuoni e l'oggetto posto dinanzi """
    def distanceCm(self):
        pulseTime = self.pulseAndWait()
        cms = (pulseTime / 2) / 29.1
        return cms
    
            
    
    
    
    
    
    
    
    
    
    
    
    

