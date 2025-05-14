import machine
import time

# Imposta il pin a cui è collegato il sensore (es. GPIO23)
sensor_pin = machine.Pin(23, machine.Pin.IN)

while True:
    # Leggi lo stato del sensore
    sensor_state = sensor_pin.value()
    
    if sensor_state == 1:
        # Il sensore rileva una superficie chiara (nessuna linea)
        print("Superficie chiara, nessuna linea rilevata")
    else:
        # Il sensore rileva una linea (superficie scura)
        print("Linea rilevata!")
    
    # Pausa per evitare di sovraccaricare la CPU
    time.sleep(0.1)
