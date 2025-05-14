import os
from KeyPad import KeyPad

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
pad = KeyPad(2,4,5,18,19,21,22,23)  # Tastierino numerico


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
        password = ''
    
        for i in range(4):
            key = pad.lettura()
            while key == None:
                key = pad.lettura()
            password = password + key

        with open('pin.txt', 'w') as f:
            f.write(password)
        
        #
        # AGGIORNAMENTO DELLO STATO
        #
        stato = STATO_CONFIGURAZIONE_WIFI
        
    elif stato == STATO_CONFIGURAZIONE_WIFI:
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato = STATO_CONNESSIONE:
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_VISTA_MENU:
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_CAMBIO_CONFIGURAZIONE:
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_INSERIMENTO_PIN:
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_SBLOCCATO:
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_BLOCCATO:
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_ALLARME:
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    
    #
    # Verifica lo stato di connessione
    #
    #


    
    
