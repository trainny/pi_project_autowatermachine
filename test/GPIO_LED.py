#!/usr/bin/python
# -*- coding: UTF-8 -*-


import RPi.GPIO as GPIO
import time
import serial
from get_value_def import *

def LED_Flash(channel): 
    for i in range(5):
        GPIO.output(channel, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(channel, GPIO.HIGH)
        time.sleep(0.2)
    GPIO.output(channel, GPIO.HIGH)
    time.sleep(0.1)
    

def water_output(temp, channel):
    
    if temp < 10:
        LED_Flash(channel)
    
    else:
        GPIO.output(channel, GPIO.HIGH)
        time.sleep(0.1)


if __name__ == '__main__':
    
    try:
        channel_1 = 12
        channel_2 = 13
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)  # 以BOARD编码格式
        GPIO.setup(channel_1, GPIO.OUT)
        GPIO.output(channel_1, GPIO.HIGH)
        GPIO.setup(channel_2, GPIO.OUT)
        GPIO.output(channel_2, GPIO.HIGH)

        while True:
            print(get_moisture_value())
            water_output(get_moisture_value(), channel_1)
            time.sleep(0.1)    

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
