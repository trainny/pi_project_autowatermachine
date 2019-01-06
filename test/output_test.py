import RPi.GPIO as GPIO
import time
import serial
from get_value_def import *
from motor_output import *


if __name__ == '__main__':
    
    try:
        channel_1 = 12
        while True:
            print(get_moisture_value())
            water_output(get_moisture_value(), channel_1)
            time.sleep(0.2)    

    except KeyboardInterrupt:
        pass


    GPIO.cleanup()
