import os
from time import sleep, localtime
from KeyPad import KeyPad
from OledClass import Oled
from wificlass import WiFi

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
#file_password_wifi = "password.txt"
#file_nome_wifi = "wifi.txt"
file_pin = "pin.txt"



""" Definizione di sensori e attuatori """
pad = KeyPad(2,4,5,18,19,14,12,23)  # Tastierino numerico
oled = Oled()   # Oled
wifi = WiFi('Galaxy A5173BB', 'aaaaaaab')


""" Definizione stato corrente """
stato = ""


""" Inizializzazione dello stato """
if not file_pin in os.listdir():
    stato = STATO_CONFIGURAZIONE_PIN
else:
    stato = STATO_CONFIGURAZIONE_WIFI
    

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
            pos = oled.write(pos[0],pos[1],0,' * ',clean=False)
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
        oled.write(1,1,0,'Benvenut*!')
        oled.show()
        sleep(2)
        
        pos = oled.write(1, 1, 0, 'Connessione al\n')
        pos = oled.write(pos[0], pos[1], 0, 'wifi in corso...', clean=False)
        oled.show()
        
        wifi.connectionWiFi()
        
        if wifi.isconnected():
            pos = oled.write(1, 1, 0, 'Connessione\nriuscita! :)')
            oled.show()
        else:
            pos = oled.write(1, 1, 0, 'Connessione\nnon riuscita.. :(')
            oled.show()
        
        sleep(2)
        
        #
        # AGGIORNAMENTO DELLO STATO
        #
        stato = STATO_CONNESSIONE
        
        
        
        
    elif stato == STATO_CONNESSIONE:
        print('Simula connessione mqtt..')
        pos = oled.write(1, 1, 0, 'Simula\nconnessione mqtt...')
        oled.show()
        sleep(4)
        oled.write(1,1,0,'')
        oled.show()
        
        #
        # AGGIORNAMENTO DELLO STATO
        #
        stato = STATO_VISTA_MENU
        
        
        
    elif stato == STATO_VISTA_MENU:
        timestamp = localtime()
        stringa = '25 C|40%|'+str(timestamp[3])+':'+str(timestamp[4])+'\n'
        pos = oled.write(1, 1, 0, stringa)
        oled.show()
        sleep(5)
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
    
    
    
    if wifi.isconnected():
        print('Ancora connesso!')
    else:
        print('Disconnesso...')
        wifi.connectionWiFi()
    
    sleep(1)


    
    
