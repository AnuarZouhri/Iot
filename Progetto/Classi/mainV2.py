import os
from time import sleep, localtime, ticks_ms, ticks_diff
from KeyPad import KeyPad
from OledClass import Oled
from WiFiClass import WiFi
from dht22 import DHT22
from UltrasonicSensor import HCSR04
from Handler import SensorHandler
from MQTTClass import MQTT

"""Callback handler"""

def sub_callback_handler(topic,msg):
        global stato, SUB_TOPICS
        if topic == SUB_TOPICS[0]:
            #
            # AGGIORNAMENTO DELLO STATO
            #
            stato = STATO_SBLOCCATO
            
        if topic == SUB_TOPICS[1]:
            #
            # AGGIORNAMENTO DELLO STATO
            #
            stato = STATO_BLOCCATO
            
        if topic == SUB_TOPICS[5]:
            print(msg)


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
pad = KeyPad(15,4,5,18,19,14,12,23)  # Tastierino numerico
oled = Oled()   # Oled Pin 22 e Pin 21
dht22 = DHT22(33)
hcsr04 = HCSR04(32,34)

"""Altri oggetti utili"""
wifi = WiFi('Galaxy A5173BB', 'aaaaaaab')
mqtt = MQTT(sub_callback_handler)
handler = SensorHandler(dht22,hcsr04)
values = []



""" Definizione stato corrente """
stato = -1
was_connected_WiFi = 0
was_connected_MQTT = 0
SUB_TOPICS = mqtt.getSUB_TOPICS()

""" Inizializzazione dello stato """
if not file_pin in os.listdir():
    stato = STATO_CONFIGURAZIONE_PIN
else:
    stato = STATO_CONFIGURAZIONE_WIFI


while True:
    values = handler.read()
    was_connected_MQTT = mqtt.checkAndRead_msg(wifi, was_connected_MQTT, values)
    
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
            print('Hai premuto',key)
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
        sleep(1)
        
        pos = oled.write(1, 1, 0, 'Connessione al\n')
        pos = oled.write(pos[0], pos[1], 0, 'wifi in corso...', clean=False)
        oled.show()
        
        wifi.connectionWiFi()
        
        if wifi.isconnected():
            pos = oled.write(1, 1, 0, 'Connessione\nriuscita!')
            oled.show()
            stato = STATO_CONNESSIONE
            was_connected_WiFi = 1
        else:
            pos = oled.write(1, 1, 0, 'Connessione\nnon riuscita..')
            oled.show()
            stato = STATO_VISTA_MENU
            print('Aggiorno stato su vista menu')
            was_connected_WiFi = 0
        sleep(1)
         
        
    elif stato == STATO_CONNESSIONE:
        pos = oled.write(1, 1, 0, 'Connessione MQTT...')
        oled.show()
        try:
            mqtt.connect()
            mqtt.subscribes()
            oled.write(1,1,0,'Connessione MQTT riuscita!')
            oled.show()
            was_connected_MQTT = 1
            sleep(0.1)
        except OSError as e:
            oled.write(1,1,0,'Connessione MQTT non riuscita!')
            oled.show()
            sleep(0.1)
            print('Connessione MQTT non riuscita')
  
        
        #
        # AGGIORNAMENTO DELLO STATO
        #
        stato = STATO_VISTA_MENU
        
        
        
    elif stato == STATO_VISTA_MENU:
        timeout = 3500  # millisecondi (es. 5 secondi)

        timestamp = localtime()
        stringa = str(values['Temperature'])+'C'+'|'+str(values['Humidity'])+'%|'+str(timestamp[3])+':'+str(timestamp[4])+'\n'
        pos = oled.write(1,1,0,'1-Apri Porta\n')
        oled.write(pos[0], pos[1], 0, stringa,clean=False)
        oled.show()
        
        key = pad.lettura()
        start_time = ticks_ms()

        while key == None and ticks_diff(ticks_ms(), start_time) < timeout:
            was_connected_MQTT = mqtt.checkAndRead_msg(wifi, was_connected_MQTT, values)
            key = pad.lettura()
        print('Hai premuto',key)
        
        
        
        if not wifi.isconnected():
            oled.write(1, 1, 0, 'Nessuna connes\nsione WiFi')
            oled.show()
            stato = STATO_CONFIGURAZIONE_WIFI
            sleep(0.5)

        sleep(1)
        
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

    elif stato == STATO_ALLARME:
        pass
        #
        # Istruzioni
        #
        # stato = NUOVO_STATO
    

    
    sleep(0.3)