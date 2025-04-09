from machine import ADC, Pin
import utime
import time

class PTM:
    def __init__(self,sig_pin):
        self.adc = ADC(Pin(sig_pin,Pin.IN))
        self.adc.atten(ADC.ATTN_11DB)
        
    def read(self):
        return self.adc.read()
    
    def value(self):
        return self.read() * (3.3/4095)



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


pt=PTM(4)


def delay(v):
    return (-0.099*v + 204.8 )/2048

while True:
    value=pt.read()
    if value >= 2048:
        x=delay(value-2048-1)
        print(x)
        step(1, 8, x)
    else:
        y=delay(value)
        print(y)
        step(-1, 8, y)


    
    

