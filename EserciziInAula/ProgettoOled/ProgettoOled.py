from machine import ADC, Pin
import time

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