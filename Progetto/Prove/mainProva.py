import os
from time import sleep, localtime
from KeyPad import KeyPad
from OledClass import Oled
from WiFiClass import WiFi
import ujson
from umqtt.simple import MQTTClient
from dht22 import DHT22
from UltrasonicSensor import HCSR04


"""Callback handler"""

def sub_callback_handler(topic,msg):
    
        if topic == TOPIC_SUB1:
            
            
            #
            # AGGIORNAMENTO DELLO STATO
            #
            stato = STATO_SBLOCCATO
            
        if topic == TOPIC_SUB2:
            
            
            #
            # AGGIORNAMENTO DELLO STATO
            #
            stato = STATO_BLOCCATO

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
dht22 = DHT22(15)
hcsr04 = HCSR04(5,18)


""" Definizione stato corrente """
stato = -1

was_connected = 0


""" Inizializzazione dello stato """
if not file_pin in os.listdir():
    stato = STATO_CONFIGURAZIONE_PIN
else:
    stato = STATO_CONFIGURAZIONE_WIFI
    

"""Definizione variabili connessione MQTT"""
CLIENT_ID 	= 'esp32'
BROKER  	= b'broker.hivemq.com'
USER 		= ''
PASSWORD 	= ''
TOPIC 		= b'TheBox'
TOPIC_SUB1 	= b'TheBox/OpenCavueaux'
TOPIC_SUB2 	= b'TheBox/CloseCaveaux'
client = None


def reset_mqtt_client():
    global client
    try:
        if client:
            client.disconnect()
    except:
        pass
    client = MQTTClient(CLIENT_ID, BROKER, user=USER, password=PASSWORD, keepalive=60)
    client.set_callback(sub_callback_handler)
try:
    reset_mqtt_client()
    
    while True:
        
        sleep(0.1)
    
        print('sto girando')
        '''if wifi.isconnected():
            print('primo')
            client.check_msg()
        '''

        if stato == STATO_CONFIGURAZIONE_PIN:
            print('Inserire pin!!')
            pos = oled.write(1,1,0,'Inserire il pin!\n')
            oled.show()
            print(pos)
            password = ''
            
            for i in range(4):
                    key = pad.lettura()
                    print('ho letto',key)
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
            sleep(0.1)
            
            pos = oled.write(1, 1, 0, 'Connessione al\n')
            pos = oled.write(pos[0], pos[1], 0, 'wifi in corso...', clean=False)
            oled.show()
            
            wifi.connectionWiFi()
            
            if wifi.isconnected():
                pos = oled.write(1, 1, 0, 'Connessione\nriuscita! :)')
                oled.show()
                stato = STATO_CONNESSIONE
                print('Aggiorno stato connessione')
            else:
                pos = oled.write(1, 1, 0, 'Connessione\nnon riuscita.. :(')
                oled.show()
                stato = STATO_VISTA_MENU
                print('Aggiorno stato menu')
            sleep(0.1)
            
            #
            # AGGIORNAMENTO DELLO STATO
            #
            
            
            
            
            
        elif stato == STATO_CONNESSIONE:
            pos = oled.write(1, 1, 0, 'Connessione mqtt...')
            oled.show()
            
            client.connect()
            client.subscribe(TOPIC_SUB1)
            client.subscribe(TOPIC_SUB2)
            oled.write(1,1,0,'Connessione riuscita!')
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
            print('sonon in menu')
            sleep(0.1)
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
            print('Porta aperta')
            #
            # Istruzioni
            #
            # stato = NUOVO_STATO
        elif stato == STATO_BLOCCATO:
            print('Porta chiusa')
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
        
        
        
        if not wifi.isconnected() and (not stato == STATO_ALLARME) and was_connected:
            oled.write(1,1,0,'Nessuna connessione!')
            
            #
            # AGGIORNAMENTO DELLO STATO
            #
            stato = STATO_CONFIGURAZIONE_WIFI
        
        sleep(0.3)
        
except KeyboardInterrupt:
    print("Interrotto manualmente.")
    try:
        if client:
            client.disconnect()
    except:
        pass

        
        
