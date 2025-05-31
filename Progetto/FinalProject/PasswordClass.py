import os

""" Classe per gestire l'inserimento della password nel file pin.txt """
class Password:
    
    """ Costruttore """
    def __init__(self):
        self.file = 'pin.txt'
        
    """ Scrive la password nel file pin.txt """
    def write(self, password):
        with open(self.file, 'w') as f:
            f.write(password)
    
    """ Restituisce la password scritta nel file pin.txt """
    def read(self):
        with open(self.file, 'r') as f:
            return f.read()
    
    """ Controlla se la password passata in input coincide con quella scritta nel file """
    def checkPassword(self, password):
        return password == self.read()
    
    """ Controlla se il file pin.txt esiste """
    def fileExists(self):
        return self.file in os.listdir()
    
    
    
            
    
        