import machine
from machine import Pin
from time import sleep_ms

'''
come funziona il sensore? il trigger emette ciclicamente
onde sonore, i quali si propagano nell'aria alla velocità
del suono. Quando vi è un oggetto avanti tale impulso viene riflesso
e rilevato da eco.
La distanza si calcola in base al tempo tra la trasmissione
dell'impulso e la ricezione del segnale d'eco.
distanza=(velocitàPropagazioneOndaSonora*tempoTraTrasmissioneERicezione)/2

'''

class HCSR04:
    '''
    Prende il pin di trigger, eco e il timeout indica il tempo massimo atteso entro cui si può rilevare un eco
    '''
    def __init__(self, trigger, echo, timeout=500*2*30):
        self.trigger = Pin(trigger, Pin.OUT)
        self.echo = Pin(echo, Pin.IN)
        self.timeout = timeout
        self.newDistance=0
        self.oldDistance=0
        
    
    '''
    Il trigger invia un'onda sonora e nel caso echo rileva un riflesso
    conta per quanti ms resta a 1. Se echo 
    '''
    def pulseAndWait(self):
        self.trigger.value(0)
        sleep_ms(5)
        self.trigger.value(1)
        sleep_ms(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.timeout) # mi dice quanto tempo echo resta a 1
            return pulse_time
        except OSError as ex: #nel caso echo non va a 1 in timeout ms
            if ex.args[0] == 110:
                raise OSError('Out of range')
            raise ex


    '''Restituisce la distanza in mm dall'oggetto che ha avanti
    def distanceMm(self):
        pulseTime = self.pulseAndWait()
        mm = pulseTime * 100 // 582
        return mm
    '''
    
    '''Restituisce la distanza in cm dall'oggetto che ha avanti'''
    def distanceCm(self):
        pulseTime = self.pulseAndWait()
        cms = (pulseTime / 2) / 29.1
        return cms
    
    '''Setta la distanza attuale'''
    def calculateDistance(self):
        self.oldDistance=self.distanceCm()
    
    '''Verifica se l'oggetto è stato spostato ovvero la distanza è aumentata'''
    def distanceChange(self):
        self.newDistance=self.distanceCm()
        if self.newDistance > self.oldDistance:
            return True
        else:
            return False
            
    
    
    
    
    
    
    
    
    
    
    
    
