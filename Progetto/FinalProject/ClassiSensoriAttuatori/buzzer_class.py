from machine import Pin, PWM
from time import sleep_ms


"""
    Classe buzzer.
"""
class BUZZER:
    
    """
        Il costruttore riceve un pin come parametro e lo utilizza per inizializzare
        l'oggetto PWM.
    """
    def __init__(self, sig_pin):
        self.pwm = PWM(Pin(sig_pin, Pin.OUT))
        self.pwm.duty(0)  # Inizialmente spento
    
    """
        Il metodo play() permette al buzzer di suonare una melodia (vettore di note).
        Il parametro wait indica la durata della nota.
    """
    def play(self, melodies, wait, duty):
        for note in melodies:
            if note == 0:
                self.pwm.duty(0) # Pausa
            else:
                self.pwm.freq(note)
                self.pwm.duty(duty) 
            sleep_ms(wait) # Durata della nota
        self.stop() # Ferma il suono alla fine
      
    """
        Interrompe il suono
    """
    def stop(self):
        self.pwm.duty(0)  # Spegne il suono
        

