from time import sleep, localtime, ticks_ms, ticks_diff
from machine import Pin
from KeyPad import KeyPad
from OledClass import Oled
from WiFiClass import WiFi
from dht22 import DHT22
from UltrasonicSensor import HCSR04
from Handler import SensorHandler
from MQTTClass import MQTT
from PasswordClass import Password
from servoMotore import ServoMotor
from mutex import Mutex
from buzzer_class import BUZZER
from MessageMaker import MM
import ujson


""" Metodo richiamato quando si preme il pulsante di chiusura della porta """
def closeDoor(pin):
    global last_press_time, stato, openDoor
    
    current_time = ticks_ms()
    if ticks_diff(current_time, last_press_time) < 200:
        return
    last_press_time = current_time
    
    if stato == STATO_SBLOCCATO:
        sv.closeDoor()
        mutex.lock()
        oled.writeLogo()
        oled.show()
        sleep(0.75)
        openDoor = False
        mqtt.publish(SUB_TOPICS[0], mm.statusDoor(0))
        stato = STATO_VISTA_MENU
        
        
""" Metodo richiamato quando si preme il pulsante per spegnere il buzzer """
def stopBuzzer(pin):
    global stato, last_press_time_buzzer, flagBuzzer
    
    current_time=ticks_ms()
    if ticks_diff(current_time, last_press_time) < 200:
        return
    last_press_time_buzzer = current_time
    
    if stato==STATO_ALLARME:
        flagBuzzer=True
        
        
"""Callback handler"""
def sub_callback_handler(topic,msg):
        global stato, SUB_TOPICS, pin, mqtt, openDoor, flagBuzzer, pinRemote, correctPin, handler
        if topic == SUB_TOPICS[0]:
            message=ujson.loads(msg)
            if 'wrong' in message and message['wrong']==1:
                stato = STATO_SBLOCCATO
                
        elif topic == SUB_TOPICS[1]:
            sv.closeDoor()
            mutex.lock()
            oled.writeLogo()
            oled.show()
            sleep(0.75)
            openDoor = False
            mqtt.publish(SUB_TOPICS[0], mm.statusDoor(0))
            stato = STATO_VISTA_MENU
            
        elif topic == SUB_TOPICS[5]:
            password = msg.decode('utf-8')
            if pinRemote:
                if pin.checkPassword(password):
                    stato=STATO_VISTA_MENU
                    correctPin=True
                    mqtt.publish(SUB_TOPICS[8], mm.correctPinMsg())
                    mutex.lock()
                else:
                    mqtt.publish(SUB_TOPICS[7], mm.wrongPinMsg())
            else:
                if pin.checkPassword(password):
                    stato = STATO_SBLOCCATO
                else:
                    mqtt.publish(SUB_TOPICS[7], mm.wrongPinMsg())
                    
        elif topic == SUB_TOPICS[10]:
            mqtt.publish(SUB_TOPICS[11], mm.correctPinMsg())
            
        elif topic == SUB_TOPICS[12]:
            if stato==STATO_ALLARME:
                flagBuzzer=True
                pinRemote=True
                
        elif topic == SUB_TOPICS[13]:
            nuovaSogliaTemp = float(msg.decode('utf-8'))
            handler.setSogliaTemp(nuovaSogliaTemp)
            
        elif topic == SUB_TOPICS[14]:
            nuovaSogliaHum = float(msg.decode('utf-8'))
            handler.setSogliaHum(nuovaSogliaHum)
            
        elif topic == SUB_TOPICS[15]:
            nuovaSogliaDis = float(msg.decode('utf-8'))
            handler.setSogliaDis(nuovaSogliaDis)
                

""" Stati principali """
STATO_CONFIGURAZIONE_PIN = 0
STATO_CONFIGURAZIONE_WIFI = 1
STATO_CONNESSIONE = 2
STATO_VISTA_MENU = 3
STATO_CAMBIO_CONFIGURAZIONE = 4
STATO_INSERIMENTO_PIN = 5
STATO_SBLOCCATO = 6
""" Stato allarme """
STATO_ALLARME = 8


""" Definizione di sensori e attuatori """
pad = KeyPad(15,4,5,18,19,14,27,33)
oled = Oled()
dht22 = DHT22(23)
hcsr04 = HCSR04(32,34)
sv=ServoMotor(26)
mutex = Mutex(16, 2, 25)
buzzer = BUZZER(17)
btnBuzzer=Pin(13, Pin.IN, Pin.PULL_DOWN)
button = Pin(12, Pin.IN, Pin.PULL_DOWN)

btnBuzzer.irq(trigger=Pin.IRQ_RISING, handler=stopBuzzer)
button.irq(trigger=Pin.IRQ_RISING, handler=closeDoor)


"""Altri oggetti utili"""
wifi = WiFi('Galaxy A5173BB', 'aaaaaaab')
mqtt = MQTT(sub_callback_handler)
handler = SensorHandler(dht22, hcsr04)
mm = MM()
pin = Password()
values = []
flagCambioConfigurazione = False
flagBuzzer= False
openDoor=False
firstRegistration=True
tempAllarm=False
humAllarm=False
distanceAllarm=False
wrongPinAllarm=False
pinRemote=False
correctPin=False
last_press_time_buzzer=0
last_press_time = 0
i=1



""" Definizione stato corrente """
stato = -1
was_connected_MQTT = 0
SUB_TOPICS = mqtt.getSUB_TOPICS()



""" Inizializzazione dello stato """
if not pin.fileExists():
    stato = STATO_CONFIGURAZIONE_PIN
else:
    stato = STATO_CONFIGURAZIONE_WIFI


""" Stato iniziale """
mutex.lock()
sv.closeDoor()
oled.writeLogo()
oled.show()
sleep(0.5)


while True:
    
    values = handler.readDht22()
    handlerCheck = handler.checkTempHum(values['Temperature'], values['Humidity'])
    
    if handlerCheck==1:
        tempAllarm=True
        stato=STATO_ALLARME
    elif handlerCheck==2:
        humAllarm=True
        stato=STATO_ALLARME  
    elif handler.checkDistance() and stato!=STATO_SBLOCCATO:
        distanceAllarm=True
        stato=STATO_ALLARME
        
    
    was_connected_MQTT = mqtt.checkAndRead_msg(wifi, was_connected_MQTT, values)
    
    if stato == STATO_CONFIGURAZIONE_PIN:
        sv.closeDoor()
        
        if not pin.fileExists():
            pos = oled.write(1, 1, 0, 'Per registrarti,\n')
            pos = oled.write(pos[0], pos[1], 0,'inserire il pin!\n', clean=False)
            oled.show()
        else:
            oled.write(1, 1, 0, 'Inserisci il\nnuovo pin:\n')
            oled.show()
        
        password = pad.letturaPin(oled, pos)
        pin.write(password)
        oled.write(1,1,0,'Pin inserito!',clean=True)
        oled.show()
        
        if wifi.isconnected():
            stato = STATO_VISTA_MENU
        else:
            stato=STATO_CONFIGURAZIONE_WIFI


    elif stato == STATO_CONFIGURAZIONE_WIFI:
        if firstRegistration:
            oled.write(1,1,0,'\n\n   Benvenut*!')
            oled.show()
            sleep(0.5)
            firstRegistration=False
        
        pos = oled.write(1, 1, 0, '\n\n  Connessione al')
        pos = oled.write(pos[0], pos[1], 0, 'wifi in corso...', clean=False)
        oled.show()
        sleep(0.6)
        
        wifi.connectionWiFi()
        
        if wifi.isconnected():
            pos = oled.write(1, 1, 0, 'Connessione\nriuscita!')
            oled.show()
            stato = STATO_CONNESSIONE
            i=1
        else:
            pos = oled.write(1, 1, 0, 'Connessione\nnon riuscita..')
            oled.show()
            stato = STATO_VISTA_MENU
            was_connected_MQTT = 0
        sleep(0.5)
         
        
    elif stato == STATO_CONNESSIONE:
        oled.write(1,1,0,'Connessione\nMQTT...')
        oled.show()
        sleep(0.5)
        try:
            mqtt.connect()
            mqtt.subscribes()
            mqtt.publish(SUB_TOPICS[11], mm.correctPinMsg())
            mqtt.publish(SUB_TOPICS[0], mm.statusDoor(0))
            was_connected_MQTT = 1
            oled.write(1,1,0,'Connessione MQTT riuscita!')
            oled.show()
            sleep(0.3)
        except OSError as e:
            oled.write(1,1,0,'Connessione MQTT non riuscita')
            was_connected_MQTT = 0
            oled.show()
            sleep(0.3)
        stato = STATO_VISTA_MENU
        
        
        
    elif stato == STATO_VISTA_MENU:
        pos = oled.write(1,1,0,'1-Apri Porta\n')
        pos = oled.write(pos[0], pos[1], 0, '2-Cambio pin\n\n', clean=False)
        timestamp = localtime()
        #'\n' + str(timestamp[2]) + '/' + str(timestamp[1]) + '/' + str(timestamp[0]) + ' ' 
         #           + str(timestamp[3]) + ':' + str(timestamp[4]) + '\n' +
        stringa =(
                   'Temp: ' + str(values['Temperature']) + 'C\n' +
                    'Umid: ' + str(values['Humidity']) + '%\n'
                   )
        oled.write(pos[0], pos[1], 0, stringa,clean=False)
        oled.show()
        
        key = pad.lettura()
        
        start_time = ticks_ms()
        timeout = 3500
        while key == None and ticks_diff(ticks_ms(), start_time) < timeout and stato != STATO_ALLARME:
            was_connected_MQTT = mqtt.checkAndRead_msg(wifi, was_connected_MQTT, values)
            key = pad.lettura()
            if handler.checkDistance() and stato!=STATO_SBLOCCATO:
                distanceAllarm=True
                stato=STATO_ALLARME
       
        if key == '1':
            stato = STATO_INSERIMENTO_PIN
        elif key == '2':
            stato = STATO_CAMBIO_CONFIGURAZIONE
        elif not wifi.isconnected() and key==None and i%2==0:
            stato = STATO_CONFIGURAZIONE_WIFI
        elif wifi.isconnected() and was_connected_MQTT == 0:
            print('riconessione broker')
            stato = STATO_CONNESSIONE
        if wifi.isconnected() :
            print('connesso')
        i=i+1

        
    elif stato == STATO_CAMBIO_CONFIGURAZIONE:
        flagCambioConfigurazione = True
        stato = STATO_INSERIMENTO_PIN
        

    elif stato == STATO_INSERIMENTO_PIN:
        password = ''
        flag = False
        cont = 0
        while not pin.checkPassword(password) and cont<3:
            pos = oled.write(1,1,0,'Inserire il pin corrente:\n')
            oled.show()
            
            password = pad.letturaPin(oled, pos)
            
            cont = cont + 1
            if pin.checkPassword(password):
                flag = True
                oled.write(1, 1, 0, 'Pin corretto:)')
                oled.show()
                sleep(0.5)
            elif cont<3:
                if cont==1:
                    pos = oled.write(1, 1, 0, 'Pin errato.\n'+'2 tentativi\nrimanenti\n')
                else:
                    pos = oled.write(1, 1, 0, 'Pin errato.\n'+'Ultimo tentativo\n')
                oled.show()
                password = ''
                sleep(2)
        
        if cont == 3 and not flag:
            stato = STATO_ALLARME
            wrongPinAllarm=True
        elif pin.checkPassword(password):
            if flagCambioConfigurazione:
                stato = STATO_CONFIGURAZIONE_PIN
                flagCambioConfigurazione = False
            else:
                stato = STATO_SBLOCCATO
            
    elif stato == STATO_SBLOCCATO:
        if openDoor==False:
            mqtt.publish(SUB_TOPICS[0], mm.statusDoor(1))
            oled.writeLogoUnlock()
            oled.show()
            sleep(0.75)
        openDoor=True
        mutex.unlock()
        sv.openDoor()
        
        oled.write(1, 1, 0, 'Porta aperta!')
        oled.show()
        

    elif stato == STATO_ALLARME:
        if tempAllarm:
            oled.write(1, 1, 0, 'ALLARME\nTemperatura anomala')
        elif humAllarm:
            oled.write(1, 1, 0, 'ALLARME\nValore di\numidita anomalo')
        elif distanceAllarm:
            oled.write(1, 1, 0, 'ALLARME\nIntrusione')
            if was_connected_MQTT and wifi.isconnected():
                mqtt.publish(SUB_TOPICS[7], mm.correctPinMsg())
        elif wrongPinAllarm:
            oled.write(1, 1, 0, 'ALLARME\nPin errato')
            if was_connected_MQTT and wifi.isconnected() :
                mqtt.publish(SUB_TOPICS[9], mm.correctPinMsg())
        oled.show()
        while not flagBuzzer:
            mutex.alarm()
            buzzer.play([330], 1000, 512)
            was_connected_MQTT = mqtt.checkAndRead_msg(wifi, was_connected_MQTT, values)
        flagBuzzer=False
        
        if not pinRemote:
            pos = oled.write(1, 1, 0, 'Inserisci il pin\n')
            oled.show()
            password = pad.letturaPin(oled, pos)
            if pin.checkPassword(password):
                stato=STATO_VISTA_MENU
                tempAllarm=False
                humAllarm=False
                distanceAllarm=False
                wrongPinAllarm=False
                if was_connected_MQTT:
                    mqtt.publish(SUB_TOPICS[8], mm.correctPinMsg())
                mutex.lock()
            else:
                oled.write(1, 1, 0, 'Pin errato')
                oled.show()
        else:
            oled.write(1, 1, 0, 'Inserisci il pin da remoto\n')
            oled.show()
            while not correctPin:
                was_connected_MQTT = mqtt.checkAndRead_msg(wifi, was_connected_MQTT, values)
        correctPin=False
        pinRemote=False
     
    sleep(0.1)
