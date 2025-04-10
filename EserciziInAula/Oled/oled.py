from machine import Pin, I2C
import ssd1306
import framebuf
import time

#risoluzione del display OLED: 128x64 pixel
WIDTH = 128
HEIGHT = 64
SCL_PIN = 22
SDA_PIN = 21

#inizializzo l'interfaccia ic2
#0 indica che vuoi usare il bus I2C numero 0.
#1 indica che vuoi usare il bus I2C numero 1.
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

display.fill(1)                         # fill entire screen with white colour 
display.rect(10, 10, 107, 43, 0)        # draw a rectangle outline 10,10 to width=107, height=53, colour=1 (black)

# draw battery percentage
# x_pos coordinate orizzontali dei blocchi che riempiono la batteria
# percentages: valori percentuali da mostrare (25%, 50%, 75%, 100%).
x_pos = [13, 23, 33, 43, 53, 63, 73, 83, 93, 103]
percentages = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]
while True:
    #Cicla 4 volte per simulare la carica crescente.
    for ctr in range(10):
        #fill_rect: disegna un blocco pieno all’interno del rettangolo batteria.
        display.fill_rect(x_pos[ctr],12,9,39,0)
        display.fill_rect(0,1,107,9,1)
        #text(...): mostra la percentuale (es. "25%").
        display.text("{:.0%}".format(percentages[ctr]), 9, 1, 0)
        #show(): aggiorna il display.
        display.show()
        time.sleep_ms(1000)
    
    # This will clear the battery charge percentage 
    for ctr in range(10):
        display.fill_rect(x_pos[ctr],11,9,40,1)
        
    display.show()

