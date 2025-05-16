from machine import Pin, PWM

class ServoMotor():
    def __init__(self,sig_pin,freq=50):
        self.pwm=PWM(sig_pin,freq)
    
    def set_angle(self,angle):
        self.duty_min = 35
        self.duty_max = 133
        self.pwm.duty(int(self.duty_min + (angle/180)*(self.duty_max-self.duty_min)))
        
    def openDoor(self, angle=0):
        self.set_angle(angle)
        
    def closeDoor(self, angle=180):
        self.set_angle(angle)
        
'''
sv=ServoMotor(23)

while True:
    sv.openDoor()
    sleep(1)
    sv.closeDoor()
    sleep(1)
    
'''
