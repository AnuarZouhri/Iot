from KeyPad import KeyPad
import os
import time


def login():
    if not 'password.txt' in os.listdir():
        print('Account non registrato! operazione non ammessa.')
        return
    
    print('Inserire i caratteri: ')
    password = ''
    
    for i in range(4):
        
        key = pad.scan()
        while pad.scan() == key:
            time.sleep_ms(20)
        
        password += key
    
    password_letta
    with open('password.txt', 'r') as f:
        password_letta = f.read()
    
    if password == password_letta:
        print('Login avvenuto con successo!')
    else:
        print('Password errata..')
        
        
        
        
def modify():
    print('Inserire i caratteri: ')
    
    password = ''
    
    for i in range(4):
        
        key = pad.scan()
        while pad.scan() == key:
            time.sleep_ms(20)
        
        password += key

    with open('password.txt', 'w') as f:
        f.write(password)
    
    print('Salvataggio avvenuto con successo!')

pad = KeyPad(2,4,5,18,19,21,22,23)

while True:
    print('Premere (1) per loggare.')
    print('Premere (2) per inserire/modificare la password.')
    
    key = pad.scan()
    while pad.scan() == key:
        time.sleep_ms(20)
    
    if key == '1':
        login()
    if key == '2':
        modify()
    if key != '1' and key != '2':
        print('Valore non ammesso!')
        
    
        
