from machine import Pin
import time

""" Classe KeyPad per il tastierino numerico """
class KeyPad:
    
    """ Costruttore """
    def __init__(self, in1, in2, in3, in4, out1, out2, out3 , out4):
        
        """ Mappa dei tasti: righe per colonne """
        self.KEY_MAP = [
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D']
        ]
        
        """ Definizione dei pin usati """
        self.rowPins = [Pin(p, Pin.IN, Pin.PULL_UP) for p in [in1, in2, in3, in4]]
        self.colPins = [Pin(p, Pin.OUT) for p in [out1, out2, out3, out4]]
        
        
    """ Scan del tasto premuto """
    def scan(self):
        for colNum, col in enumerate(self.colPins):
            """ Tutte le colonne a 1 tranne una (col) """
            for c in self.colPins:
                c.value(1)
            col.value(0)
            
            """ Sulla colonna selezionata (col) si controlla quale riga è selezionata (quindi 0) """
            for rowNum, row in enumerate(self.rowPins):
                if row.value() == 0:
                    time.sleep_ms(50)  # Si evita il debounce
                    if row.value() == 0:  # verifica di nuovo
                        return self.KEY_MAP[rowNum][colNum]
        return None

    """ Lettura attiva del tasto premuto """
    def lettura(self):
        key = self.scan()
        if key:
            print('Hai premuto: ', key, ' di tipo: ', type(key))
            while pad.scan() == key:
                time.sleep_ms(20)
            time.sleep_ms(50)
        return key