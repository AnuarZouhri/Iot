from machine import Pin, PWM, ADC
import time

pwm2 = PWM(Pin(27), freq=50)

class BUZZER:
    def __init__(self, sig_pin):
        self.pwm = PWM(Pin(sig_pin, Pin.OUT))
        self.pwm.duty(0)  # Inizialmente spento
        
    def play(self, melodies, wait, duty):
        for note in melodies:
            if note == 0:
                self.pwm.duty(0) # Pausa
            else:
                self.pwm.freq(note)
                self.pwm.duty(duty) # Imposta il volume del suono
            time.sleep_ms(wait) # Durata della nota
        self.stop() # Ferma il suono alla fine
        
    def stop(self):
        self.pwm.duty(0)  # Spegne il suono

class LDR:
    """This class read a value from a light dependent resistor (LDR)"""

    def __init__(self, pin, min_value=0, max_value=100):
        """
        Initializes a new instance.
        :parameter pin A pin that's connected to an LDR.
        :parameter min_value A min value that can be returned by value() method.
        :parameter max_value A max value that can be returned by value() method.
        """
        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')

        # initialize ADC (analog to digital conversion)
        # create an object ADC
        self.adc = ADC(Pin(pin))
        self.min_value = min_value
        self.max_value = max_value

    def read(self):
        """
        Read a raw value from the LDR.
        :return a value from 0 to 4095.
        """
        return self.adc.read()

    def value(self):
        """
        Read a value from the LDR in the specified range.
        :return a value from the specified [min, max] range.
        """
        return (self.max_value - self.min_value) * self.read() / 4095

A5=880

def set_angle(angle):
    duty_min = 35
    duty_max = 133
    pwm2.duty(int(duty_min + (angle/180)*(duty_max-duty_min)))


ldr = LDR(34)
led = Pin(17, Pin.OUT)
buzzer = BUZZER(5)
set_angle(0) #imposta 0 gradi
led.off()
time.sleep(1)
while True:
    value1 = ldr.read()
    print('analog value= {}'.format(value1))
    value = ldr.value()
    print('value = {}'.format(value))
    
    angle = value/100 * 180
    print("angle: ", angle)
    set_angle(angle)
    while value < 20:
        led.on()
        buzzer.play([A5], 500, 512)
        value = ldr.value()
        angle = value/100 * 180
        print("angle: ", angle)
        set_angle(angle)
    led.off()
    time.sleep(0.5)
        
    