from machine import Pin, PWM

"""classe per l'oggetto Led"""
 class LED:
    """ Costruttore """
    def __init__(self, sig_pin, flag=True, freq=5000):
        """Passando solo il numero del Pin, il led è istanziato come Pin"""
        if flag:
            self.led=Pin(sig_pin, Pin.OUT)
        else:
            self.pmw=PWM(sig_pin, freq)
    
    def ledOn(self):
        self.led.on()
        
    def ledOff(self):
        self.led.off()
                
    def ledDuty(self,duty):
        self.led.duty(duty)
    
        
