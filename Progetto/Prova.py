from machine import Pin
import os
import time


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
        
        
    """ Lettura del tasto premuto """
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
    
    def lettura(self):
        key = self.scan()
        if key:
            print('Hai premuto: ', key, ' di tipo: ', type(key))
            while pad.scan() == key:
                time.sleep_ms(20)
            time.sleep_ms(50)
        return key
        

def login():
    if not 'password.txt' in os.listdir():
        print('Account non registrato! operazione non ammessa.')
        return
    
    print('Inserire i caratteri: ')
    password = ''
    
    for i in range(4):
        
        key = pad.lettura()
        while key == None:
            key = pad.lettura()
        
        password += key
    
    password_letta = ''
    with open('password.txt', 'r') as f:
        password_letta = f.read()
    
    if password == password_letta:
        print('Login avvenuto con successo!')
    else:
        print('Password errata..')
        
        
        
        
def modify():
    print('Inserire i caratteri: ')
    
    password = ''
    
    for i in range(4):
        
        key = pad.lettura()
        while key == None:
            key = pad.lettura()
        
        password = password + key

    with open('password.txt', 'w') as f:
        f.write(password)
    
    print('Salvataggio avvenuto con successo!')

pad = KeyPad(2,4,5,18,19,21,22,23)

while True:
    #print('Premere (1) per loggare.')
    #print('Premere (2) per inserire/modificare la password.')
    
    key = pad.lettura()
    #if key is not None:
    #    pass
    #while key == None:
    #    key = pad.lettura()
    
    if key == '1':
        login()
    #if key == '2':
    #    modify()
    #if key != '1' and key != '2':
    #    print('Valore non ammesso!')
        
    
        
