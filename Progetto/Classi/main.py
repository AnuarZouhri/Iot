import os
from KeyPad import KeyPad
from OledClass import Oled

""" Stati principali """
STATO_CONFIGURAZIONE_PIN = 0
STATO_CONFIGURAZIONE_WIFI = 1
STATO_CONNESSIONE = 2
STATO_VISTA_MENU = 3
STATO_CAMBIO_CONFIGURAZIONE = 4
STATO_INSERIMENTO_PIN = 5
STATO_SBLOCCATO = 6
STATO_BLOCCATO = 7

""" Stato allarme """
STATO_ALLARME = 8


""" File per il salvataggio dei dati di configurazione """
file_password_wifi = "password.txt"
file_nome_wifi = "wifi.txt"
file_pin = "pin.txt"



""" Definizione di sensori e attuatori """
pad = KeyPad(2,4,5,18,19,14,12,23)  # Tastierino numerico
oled = Oled()   # Oled


""" Definizione stato corrente """
stato = ""


""" Inizializzazione dello stato """
if not file_pin in os.listdir():
    stato = STATO_CONFIGURAZIONE_PIN
else:
    stato = STATO_CONNESSIONE
    

while True:
    
    if stato == STATO_CONFIGURAZIONE_PIN:
        print('Inserire pin!!')
        pos = oled.write(1,1,0,'Inserire il pin!\n')
        oled.show()
        print(pos)
        password = ''
    
        for i in range(4):
            key = pad.lettura()
            while key == None:
                key = pad.lettura()
            password = password + key
            pos = oled.write(pos[0],pos[1],0,'*',clean=False)
            oled.show()

        with open('pin.txt', 'w') as f:
            f.write(password)
        
        oled.write(1,1,0,'Pin inserito!',clean=True)
        oled.show()
        #
        # AGGIORNAMENTO DELLO STATO
        #
        stato = STATO_CONFIGURAZIONE_WIFI
        
        
        
        
    elif stato == STATO_CONFIGURAZIONE_WIFI:
        pass
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
        
        
        
        
        
    elif stato == STATO_CONNESSIONE:
        pass
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_VISTA_MENU:
        pass
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_CAMBIO_CONFIGURAZIONE:
        pass
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_INSERIMENTO_PIN:
        pass
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_SBLOCCATO:
        pass
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_BLOCCATO:
        pass
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_ALLARME:
        pass
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    
    #
    # Verifica lo stato di connessione
    #
    #


    
    
