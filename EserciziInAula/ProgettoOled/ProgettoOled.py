from machine import ADC, Pin, PWM
import time


pwm2 = PWM(Pin(27), freq=50) '<- servo motore'

class LED:
    def __init__(self, sig_pin, flag=True, freq=5000):
        """Passando solo il numero del Pin il led è istanziato come Pin"""
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

class LDR:
    
    def __init__(self, pin, min_value=0, max_value=100):
        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')

        self.adc = ADC(Pin(pin))
        self.min_value = min_value
        self.max_value = max_value

    def read(self):
        """
        legge un valore da 0 a 4095
        """
        return self.adc.read()

    def value(self):
        """
        resituisce il valore letto dal fotoresistore come valore dell'intervallo [min_value,max_value]
        """
        return (self.max_value - self.min_value) * self.read() / 4095




def set_angle(angle):
    duty_min = 35
    duty_max = 133
    pwm2.duty(int(duty_min + (angle/180)*(duty_max-duty_min)))


ldr = LDR(34,0,180)
led = LED(14)
led.ledOff()

while True:
    value = ldr.value()
    if value > 60:
        led.ledOn()
        set_angle(180)
    led.ledOff()
    set_angle(0)
        
    
    







