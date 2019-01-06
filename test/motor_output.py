#!/usr/bin/python
# -*- coding: UTF-8 -*-


import RPi.GPIO as GPIO
import time
from GPIO_LED import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # 以BOARD编码格式


def water_output(temp, channel):

    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.HIGH)

    if temp < 10:
        LED_Flash(channel)
    
    else:
        GPIO.output(channel, GPIO.HIGH)
        time.sleep(0.1)
#-------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------------#