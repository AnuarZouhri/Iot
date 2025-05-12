from machine import Pin
import time

# Mappa dei tasti: righe x colonne
KEY_MAP = [
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['*','0','#','D']
]

# Definizione dei pin usati (modifica secondo i tuoi collegamenti)
ROW_PINS = [Pin(p, Pin.IN, Pin.PULL_UP) for p in [2, 4, 5, 18]]
COL_PINS = [Pin(p, Pin.OUT) for p in [19, 21, 22, 23]]

def scan_keypad():
    for col_num, col in enumerate(COL_PINS):
        # Metti solo questa colonna a LOW
        for c in COL_PINS:
            c.value(1)
        col.value(0)

        # Controlla quale riga è bassa (tasto premuto)
        for row_num, row in enumerate(ROW_PINS):
            if row.value() == 0:
                time.sleep_ms(50)  # debounce
                if row.value() == 0:  # verifica di nuovo
                    return KEY_MAP[row_num][col_num]
    return None

# Loop principale
print("Pronto a leggere i tasti...")
while True:
    key = scan_keypad()
    if key:
        print("Hai premuto:", key)
        while scan_keypad() == key:
            time.sleep_ms(10)  # aspetta il rilascio
    time.sleep_ms(50)