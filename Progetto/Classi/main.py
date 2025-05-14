import os

""" Stati principali """
STATO_CONFIGURAZIONE_SISTEMA = 0
STATO_CONNESSIONE = 1
STATO_VISTA_MENU = 2
STATO_CAMBIO_CONFIGURAZIONE = 3
STATO_INSERIMENTO_PIN = 4
STATO_SBLOCCATO = 5
STATO_BLOCCATO = 6
STATO_RICONNESSIONE = 7

""" Stato allarme """
STATO_ALLARME = 8


""" File per il salvataggio dei dati di configurazione """
file_password_wifi = "password.txt"
file_nome_wifi = "wifi.txt"
file_pin = "pin.txt"


""" Definizione stato corrente """
stato = ""


""" Inizializzazione dello stato """
if not file_pin in os.listdir():
    stato = STATO_CONFIGURAZIONE_SISTEMA
else:
    stato = STATO_CONNESSIONE
    

while True:
    
    #
    # CONTROLLO DELLO STATO DI RICONNESSIONE
    #
    #
    
    if stato == STATO_CONFIGURAZIONE_SISTEMA:
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_CONNESSIONE:
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
    elif stato == STATO_RICONNESSIONE:
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    elif stato == STATO_ALLARME:
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    


    
    
