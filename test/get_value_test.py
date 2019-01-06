#-------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------------#
import RPi.GPIO as GPIO
import serial
import time
from get_value_def import *


if __name__ == '__main__':
    
    try:
        channel_1 = 11
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)  # 以BOARD编码格式
        
        data_ex = get_value(channel_1)
        
        while True:
            data_1 = get_value(channel_1)
            #print(data_1)
            if data_1[0:2] != (0,0):
                print(data_1)
                time.sleep(0.1)
                data_ex = data_1
            else:
                print(data_ex)
                time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    ser.close()
    GPIO.cleanup()
