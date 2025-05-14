from machine import Pin, I2C
import ssd1306
import framebuf
import network
import time

class Oled:
    
    def __init__(self):
        self.WIDTH = 128
        self.HEIGHT = 64
        self.SCL_PIN = 22
        self.SDA_PIN = 21
        self.i2c = I2C(0, scl=Pin(self.SCL_PIN), sda=Pin(self.SDA_PIN))
        self.display = ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c)
        
        
    def write(self,x,y,color_background,text,separator='\n',clean = True):
        if clean == True:
            self.display.fill_rect(0,0,128,64,color_background)
        i=0
        for char in text:
            
            if not char == separator:
                self.display.text(char,x+i*8,y,not color_background)
            i = i+1
            if x+i*8 >= 128 or char == separator:
                y = y+10
                i=0
            
        #self.display.show()
        return [x+i*8,y]
    
    def show(self):
        self.display.show()
    
    
    def writeLogo(self):
        pass
        

         
        
        
    