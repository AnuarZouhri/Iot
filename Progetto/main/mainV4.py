from time import sleep, localtime, ticks_ms, ticks_diff
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
from machine import Pin
from buzzer_class import BUZZER
from MessageMaker import MM
from machine import disable_irq, enable_irq


def closeDoor(pin):
    global last_press_time, stato, openDoor
    current_time = ticks_ms()
    if ticks_diff(current_time, last_press_time) < 200:
        return
    last_press_time = current_time
    
    if stato == STATO_SBLOCCATO:
        sv.closeDoor()
        mqtt.publish(SUB_TOPICS[0], mm.wrongPinMsg())
        oled.writeLogo()
        oled.show()
        sleep(0.75)
        mutex.lock()
        openDoor = False
        stato = STATO_VISTA_MENU
        
        
def stopBuzzer(pin):
    global stato, last_press_time_buzzer, flagBuzzer
    current_time=ticks_ms()
    if ticks_diff(current_time, last_press_time) < 200:
        return
    last_press_time_buzzer = current_time
    
    if stato==STATO_ALLARME:
        flagBuzzer=True
        
def checkTempHum(values):
    global stato
    temp=values['Temperature']
    hum=values['Humidity']
    if temp>50 or hum>70:
        stato=STATO_ALLARME

def checkDistance():
    global stato, standardDistance
    if hcsr04.distanceCm()<standardDistance and stato!=STATO_SBLOCCATO :
        stato=STATO_ALLARME
        
    
        

"""Callback handler"""

def sub_callback_handler(topic,msg):
        global stato, SUB_TOPICS, pin, mqtt, openDoor
        print(topic)
        print(SUB_TOPICS[0])
        if topic == SUB_TOPICS[0]:
            stato = STATO_SBLOCCATO
            
        if topic == SUB_TOPICS[1]:
            sv.closeDoor()
            mqtt.publish(SUB_TOPICS[0], mm.wrongPinMsg())
            oled.writeLogo()
            oled.show()
            sleep(0.75)
            mutex.lock()
            openDoor = False
            stato = STATO_VISTA_MENU
            
        if topic == SUB_TOPICS[5]:
            password = msg.decode('utf-8')
            newmsg = ''
            
            if pin.checkPassword(password):
                stato = STATO_SBLOCCATO
                newmsg = mm.correctPinMsg()
            else:
                newmsg = mm.wrongPinMsg()
                
            
                


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
pad = KeyPad(15,4,5,18,19,14,12,33)  # Tastierino numerico
oled = Oled()   # Oled Pin 22 e Pin 21
dht22 = DHT22(23)
hcsr04 = HCSR04(32,34)
sv=ServoMotor(26)
mutex = Mutex(16, 2, 25)
buzzer = BUZZER(17)
btnBuzzer=Pin(13, Pin.PULL_DOWN)
btnBuzzer.irq(trigger=Pin.IRQ_RISING, handler=stopBuzzer)
last_press_time_buzzer=0
mm = MM()

mutex.lock()
button = Pin(0, Pin.IN, Pin.PULL_DOWN)
button.irq(trigger=Pin.IRQ_RISING, handler=closeDoor)
last_press_time = 0

"""Altri oggetti utili"""
wifi = WiFi('Galaxy A5173BB', 'aaaaaaab')
mqtt = MQTT(sub_callback_handler)
handler = SensorHandler(dht22,hcsr04)
pin = Password()
values = []
flagCambioConfigurazione = False
flagBuzzer= False
standardDistance=17
openDoor=False



""" Definizione stato corrente """
stato = -1
was_connected_WiFi = 0
was_connected_MQTT = 0
SUB_TOPICS = mqtt.getSUB_TOPICS()


""" Inizializzazione dello stato """
if not pin.fileExists():
    stato = STATO_CONFIGURAZIONE_PIN
else:
    stato = STATO_CONFIGURAZIONE_WIFI

oled.writeLogo()
oled.show()
sleep(1)
sv.closeDoor()
while True:
    values = handler.read()
    print(values)
    checkTempHum(values)
    checkDistance()
    
    was_connected_MQTT = mqtt.checkAndRead_msg(wifi, was_connected_MQTT, values)
    
    if stato == STATO_CONFIGURAZIONE_PIN:
        sv.closeDoor()
        
        print('Inserire pin!!')
        pos = oled.write(1, 1, 0, 'Per registrarti,\n')
        pos = oled.write(pos[0], pos[1], 0,'inserire il pin!\n', clean=False)
        oled.show()
        print(pos)
        
        password = pad.letturaPin(oled, pos)

        pin.write(password)
        
        
        oled.write(1,1,0,'Pin inserito!',clean=True)
        oled.show()
        
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
            mqtt.publish(SUB_TOPICS[0], mm.wrongPinMsg())
            was_connected_MQTT = 1
            sleep(0.1)
        except OSError as e:
            oled.write(1,1,0,'Connessione MQTT non riuscita!')
            oled.show()
            sleep(0.1)
            print('Connessione MQTT non riuscita')
  
        stato = STATO_VISTA_MENU
        
        
        
    elif stato == STATO_VISTA_MENU:
        timeout = 3500  # millisecondi (es. 5 secondi)
        timestamp = localtime()
        stringa = str(values['Temperature'])+'C'+'|'+str(values['Humidity'])+'%|'+str(timestamp[3])+':'+str(timestamp[4])+'\n'
        pos = oled.write(1,1,0,'1-Apri Porta\n')
        pos = oled.write(pos[0], pos[1], 0, '2-Cambia config\n', clean=False)
        oled.write(pos[0], pos[1], 0, stringa,clean=False)
        oled.show()
        
        key = pad.lettura()
        start_time = ticks_ms()
        
        while key == None and ticks_diff(ticks_ms(), start_time) < timeout and stato != STATO_ALLARME:
            was_connected_MQTT = mqtt.checkAndRead_msg(wifi, was_connected_MQTT, values)
            key = pad.lettura()
            checkDistance()
        print('Hai premuto',key)
       
        if key == '1':
            stato = STATO_INSERIMENTO_PIN
        elif key == '2':
            stato = STATO_CAMBIO_CONFIGURAZIONE
        elif not wifi.isconnected() and key==None:
            oled.write(1, 1, 0, 'Nessuna connes\nsione WiFi')
            oled.show()
            stato = STATO_CONFIGURAZIONE_WIFI
            sleep(0.5)
        
      
        sleep(0.3)
        
        
        
   
   
        
    elif stato == STATO_CAMBIO_CONFIGURAZIONE:
        pos = oled.write(1, 1, 0, 'Hai deciso di\nmodificare il\npin.')
        sleep(0.5)
        
        flagCambioConfigurazione = True
        
        stato = STATO_INSERIMENTO_PIN
        

    elif stato == STATO_INSERIMENTO_PIN:
        password = ''
        flag = False
        cont = 0
        while not pin.checkPassword(password) and cont<3:
            print(pos)
            pos = oled.write(1,1,0,'Inserire il pin corrente!\n')
            oled.show()
            
            password = pad.letturaPin(oled, pos)
            
            cont = cont + 1
            if pin.checkPassword(password):
                print('Pin corretto!')
                flag = True
                oled.write(1, 1, 0, 'Pin inserito\ncorrettamente!\n:)')
                oled.show()
                sleep(0.5)
            else:
                print('Pin errato..')
                pos = oled.write(1, 1, 0, 'Pin errato.\n'+str(3-cont)+' tentativi\nrimanenti.\n')
                oled.show()
                password = ''
                sleep(2)
        
        if cont == 3 and not flag:
            stato = STATO_ALLARME
        elif pin.checkPassword(password):
            if flagCambioConfigurazione:
                stato = STATO_CONFIGURAZIONE_PIN
                flagCambioConfigurazione = False
            else:
                stato = STATO_SBLOCCATO
            
        
    elif stato == STATO_SBLOCCATO:
        if openDoor==False:
            print('Porta aperta')
            mqtt.publish('TheBox/OpenCaveaux', mm.correctPinMsg())
            print(mm.correctPinMsg())
            oled.writeLogoUnlock()
            oled.show()
            sleep(0.75)
        openDoor=True
        mutex.unlock()
        sv.openDoor()
        
        oled.write(1, 1, 0, 'Porta aperta!')
        oled.show()
        

    elif stato == STATO_ALLARME:
        pos=oled.write(1, 1, 0, 'Allarme\n')
        oled.show()
        while not flagBuzzer:
            mutex.alarm()
            buzzer.play([330], 1000, 512)
        flagBuzzer=False
        pos = oled.write(pos[0], pos[1], 0, 'Inserisci il pin\n', clean=False)
        oled.show()
        password = pad.letturaPin(oled, pos)
        if pin.checkPassword(password):
            stato=STATO_VISTA_MENU
            mutex.lock()
        else:
            oled.write(1, 1, 0, 'Pin errato')
            oled.show()
     
    
    sleep(0.3)


