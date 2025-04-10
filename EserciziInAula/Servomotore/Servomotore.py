from machine import Pin, PWM
import time

pwm2 = PWM(Pin(27), freq=50)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)  # Pulsante con pull-up interno
last_press_time = 0
flag1 = False

def set_angle(angle):
    duty_min = 35
    duty_max = 133
    pwm2.duty(int(duty_min + (angle/180)*(duty_max-duty_min)))

set_angle(0) #imposta 0 gradi
while True:
    set_angle(0)
    while button.value()==1:
        set_angle(180)
        time.sleep(0.5)
        set_angle(0)
        time.sleep(0.5)
    
    