import os

class Password:
    
    def __init__(self):
        self.file = 'pin.txt'
        
    
    def write(self, password):
        with open(self.file, 'w') as f:
            f.write(password)
            
    def read(self):
        with open(self.file, 'r') as f:
            return f.read()
    
    def checkPassword(self, password):
        return password == self.read()
    
    def fileExists(self):
        return self.file in os.listdir()
    
    
    
            
    
        