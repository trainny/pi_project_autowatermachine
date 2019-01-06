import time
import RPi.GPIO as GPIO

channel1 = 11
channel2 = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)		#以BOARD编码格式

GPIO.setup(channel1, GPIO.IN)
GPIO.setup(channel2, GPIO.OUT)
GPIO.output(channel2, GPIO.HIGH)

try:
    
    while True:
        
        if GPIO.input(channel1) == GPIO.LOW:
            
            for i in range(5):
                
                GPIO.output(channel2, GPIO.LOW)
                time.sleep(0.1)
                GPIO.output(channel2, GPIO.HIGH)
                time.sleep(0.1)
                
        else:
            GPIO.output(channel2, GPIO.HIGH)
            time.sleep(0.1)
        
except KeyboardInterrupt:
    pass
 
GPIO.cleanup()
