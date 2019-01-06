#!/usr/bin/python
# -*- coding: UTF-8 -*-


from time import sleep
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

pin_1 = 13
pin_2 = 15
pin_3 = 38
pin_4 = 40
pan = 12
top = 11
 
GPIO.setup(top, GPIO.OUT) # white => TILT
GPIO.setup(pin_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_4, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(pan, GPIO.OUT) # gray ==> PAN

class MQTT:
    def __init__(self):
        self.Host = "139.199.89.222"
        self.Port = 1883
        self.Client = mqtt.Client()
        self.Client.connect(self.Host,self.Port,60)
        self.CMD = ""

    def publish(self,Topic,Message):
        self.Client.publish(Topic,Message,qos=0,retain=False)

    def subcribe(self,Topic):
        self.Client.loop_start()
        self.Client.subscribe(Topic,1)
        self.Client.on_message = self.on_message_come

    def on_message_come(self,client,userdata,msg):
        self.CMD = msg.payload.decode('gbk')
        print(self.CMD)

def setServoAngle(servo, angle):
    assert angle >= 0 and angle <= 180
    pwm = GPIO.PWM(servo, 50)
    dutyCycle = angle / 18. + 2.
    pwm.start(dutyCycle)
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.05)
    pwm.stop()

if __name__ == '__main__':  
    try:
        angle_top = 90
        angle_pan = 90
        setServoAngle(top, angle_top)
        sleep(0.8)
        setServoAngle(pan, angle_pan)
        sleep(0.8)
        mqtt = MQTT()
        mqtt.subcribe("ding_water")
        while True:
            sleep(0.01)
            
            #UP
            if mqtt.CMD == "up": 
                if angle_top > 10:
                    angle_top -= 2
                    #sleep(0.1)
                    #print(angle_top)
                    setServoAngle(top, angle_top)
                    sleep(0.015)
                mqtt.CMD = ""
                
            #DOWM        
            if mqtt.CMD == "down": 
                if angle_top < 170:
                    angle_top += 2
                    #sleep(0.1)
                    #print(angle_top)
                    setServoAngle(top, angle_top)
                    sleep(0.015)
                mqtt.CMD = ""
                    
            #RIGHT        
            if mqtt.CMD == "right": 
                if angle_pan > 10:
                    angle_pan -= 2
                    #sleep(0.1)
                    #print(angle_top)
                    setServoAngle(pan, angle_pan)
                    sleep(0.015)
                mqtt.CMD = ""
                
            #LEFT
            if mqtt.CMD == "left": 
                if angle_pan < 170:
                    angle_pan += 2
                    #sleep(0.1)
                    #print(angle_top)
                    setServoAngle(pan, angle_pan)
                    sleep(0.015)
                mqtt.CMD = ""
                    
                    
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()