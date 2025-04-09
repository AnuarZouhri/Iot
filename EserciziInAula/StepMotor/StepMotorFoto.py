"""Classe per il fotoresistore (light dependent resistor)"""
from machine import ADC, Pin
import time
import utime

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
    
    
# Define the pins for the stepper motor
IN1=Pin(26, Pin.OUT)
IN2=Pin(25, Pin.OUT)
IN3=Pin(33, Pin.OUT)
IN4=Pin(32, Pin.OUT)

stepper_pins = [IN1, IN2, IN3, IN4]

# full-step con 2 bobbine attive
# due bobbine accese per ogni step -> più coppia
step_sequence = [
    [1, 0, 0, 1], # IN1 e IN2 accesi
    [1, 1, 0, 0], # IN2 e IN3 accesi
    [0, 1, 1, 0], # IN3 e IN4 accesi
    [0, 0, 1, 1], # IN4 e IN1 accesi
]

#direction = +1 (antiorario), -1 (orario)
#steps = numero di passi da eseguire
#delay = tempo tra un passo e l'altro
#step_index tiene traccia del passo attuale nella sequenza.

def step(direction, steps, delay):
    global step_index 
    for i in range(steps):
        # l'operatore % garantisce che step_index rimanga all'interno dell'intervallo valido,
        # assicurando che la sequenza dei passi venga ripetuta ciclicamente.
        step_index = (step_index + direction) % len(step_sequence) #mod 4
        for pin_index in range(len(stepper_pins)):
            #Esempio: se step_index = 2, la sequenza è [0, 1, 1, 0]
            # Se pin_index = 0 → pin_value = 0
            # Se pin_index = 1 → pin_value = 1
            # ecc.
            pin_value = step_sequence[step_index][pin_index] 
            stepper_pins[pin_index].value(pin_value)
        utime.sleep(delay)

step_index = 0


fr=LDR(34)


while True:
    value=fr.read()
    print(value)
    if value < 2048:
        step(1, 50, 0.01)
    else:
        step(-1, 50, 0.01)
    time.sleep(0.5)
    
    
    


