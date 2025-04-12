from machine import Pin, PWM

class ServoMotor():
    def __init__(self,sig_pin,freq=50):
        self.pwm=PWM(sig_pin,freq)
    
    def set_angle(self,angle):
        self.duty_min = 35
        self.duty_max = 133
        self.pwm.duty(int(duty_min + (angle/180)*(duty_max-duty_min)))