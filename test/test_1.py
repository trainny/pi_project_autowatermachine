#!/usr/bin/python
# -*- coding: UTF-8 -*-

from socket import *
import threading
import struct
import time
import cv2
import numpy
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import serial
from get_value_def import *

channel_1 = 11
        
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # 以BOARD编码格式
data_ex = get_value(channel_1)

class MQTT:
    def __init__(self):
        self.Host = "139.199.89.222"
        self.Port = 1883
        self.Client = mqtt.Client()
        self.Client.connect(self.Host,self.Port,60)
        self.servo_CMD = ""
        self.Client.loop_start()
        self.Client.subscribe("ding_water",1)
        self.Client.on_message = self.on_message_come

    def publish(self,Topic,Message):
        self.Client.publish(Topic,Message,qos=0,retain=False)

    def subcribe(self,Topic):
        self.Client.loop_start()
        self.Client.subscribe(Topic,1)
        self.Client.on_message = self.on_message_come

    def on_message_come(self,client,userdata,msg):
        self.servo_CMD = msg.payload.decode('gbk')

class Carame_Accept_Object:
    def __init__(self,S_addr_port=("",8888)):
        self.resolution=(640,480)
        self.img_fps=15
        self.addr_port=S_addr_port
        self.server=socket(AF_INET,SOCK_STREAM)

        self.server.listen(5)
        self.client = ""
        self.D_addr = ""
        self.c = ""
        
    def RT_Image(self,client,D_addr):
        self.c=cv2.VideoCapture(0)
        self.img_param=[int(cv2.IMWRITE_JPEG_QUALITY),self.img_fps]
        while True:
            time.sleep(0.1)
            (self.grabbed,self.img)=self.c.read()
            self.img=cv2.resize(self.img,self.resolution)
            self.result,self.img_encode=cv2.imencode('.jpg',self.img,self.img_param)
            self.img_code=numpy.array(self.img_encode)
            self.img_data=self.img_code.tostring()
            try:
                client.send(struct.pack("lhh",len(self.img_data),self.resolution[0],self.resolution[1])+self.img_data)
            except:
                client.close()
                self.c.release()
                break

class Servo:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.angle_top = 90
        self.angle_pan = 90
        self.channel_2 = 12
        self.channel_3 = 13
        GPIO.setup(self.channel_2, GPIO.OUT)
        GPIO.output(self.channel_2, GPIO.HIGH)
        GPIO.setup(self.channel_3, GPIO.OUT)
        GPIO.output(self.channel_3, GPIO.HIGH)
        self.pin()
        self.GPIO_setup()

    def pin(self):
        self.pan = 38
        self.top = 40

    def GPIO_setup(self):
        GPIO.setup(self.top, GPIO.OUT) # white => TILT
        GPIO.setup(self.pan, GPIO.OUT)

    def setServoAngle(self,servo,angle):
        assert angle >= 0 and angle <= 180
        self.pwm = GPIO.PWM(servo, 50)
        self.dutyCycle = angle / 18. + 2.
        self.pwm.start(self.dutyCycle)
        self.pwm.ChangeDutyCycle(self.dutyCycle)
        time.sleep(0.05)
        self.pwm.stop()

    def angle_init(self):
        pass

class Main(Carame_Accept_Object,MQTT,Servo):
    def __init__(self):
        Servo.__init__(self)
        Carame_Accept_Object.__init__(self)
        MQTT.__init__(self)

    def camera(self):
        while True:
            self.client,self.D_addr=self.server.accept()
            self.RT_Image(self.client,self.D_addr)

    def camera_thread(self):
        threading.Thread(None,target=self.camera).start()
        
    def servo(self):
        while True:
            time.sleep(0.01)
            if self.servo_CMD == "up":
                if self.angle_top > 40:
                    self.angle_top -= 10
                    self.setServoAngle(self.top,self.angle_top)
                    time.sleep(0.1)
                    print("up")
                self.servo_CMD = ""
                
            if self.servo_CMD == "down":
                if self.angle_top < 140:
                    self.angle_top += 10
                    self.setServoAngle(self.top,self.angle_top)
                    time.sleep(0.1)
                    print("down")
                self.servo_CMD = ""
                
            if self.servo_CMD == "right":
                if self.angle_pan > 40:
                    self.angle_pan -= 10
                    self.setServoAngle(self.pan,self.angle_pan)
                    time.sleep(0.1)
                    print("right")
                self.servo_CMD = ""
                
            if self.servo_CMD == "left":
                if self.angle_pan < 140:
                    self.angle_pan += 10
                    self.setServoAngle(self.pan,self.angle_pan)
                    time.sleep(0.1)
                    print("left")
                self.servo_CMD = ""
            
            if self.servo_CMD == "water":
                GPIO.output(self.channel_3, GPIO.LOW)
                time.sleep(10);
                GPIO.output(self.channel_3, GPIO.HIGH)
                time.sleep(0.1)
                self.servo_CMD = ""
                
            if self.servo_CMD == "fertilizer":
                GPIO.output(self.channel_2, GPIO.LOW)
                time.sleep(10);
                GPIO.output(self.channel_2, GPIO.HIGH)
                time.sleep(0.1)
                self.servo_CMD = ""

    def servo_thread(self):
        self.setServoAngle(self.top,self.angle_top)
        time.sleep(0.5)
        self.setServoAngle(self.pan,self.angle_pan)
        time.sleep(1)
        threading.Thread(None,target=self.servo).start()
        print("end")
            
if __name__ == '__main__':
    main = Main()
    main.camera_thread()
    main.servo_thread()
    #while True:
        #pass
    
    try:
        while True:
            data_1 = get_value(channel_1)
            #print(data_1)
            if data_1[0:2] != (0,0):
                #print(data_1)
                time.sleep(0.1)
                data_ex = data_1
                data_ex = str(data_ex)
                print(data_ex)
            else:
                data_ex = str(data_ex)
                print(data_ex)
                time.sleep(0.1)
            main.publish("ding_water_pi",data_ex)

    except KeyboardInterrupt:
        pass

    ser.close()
    GPIO.cleanup()
