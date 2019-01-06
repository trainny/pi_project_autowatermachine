import RPi.GPIO as GPIO
import serial
import time
#-------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------------#
channel_1 = 11			#引脚号11
channel_2 = 12
ser = serial.Serial('/dev/ttyUSB0', 115200)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # 以BOARD编码格式
GPIO.setup(channel_2, GPIO.OUT)
GPIO.output(channel_2, GPIO.HIGH)

#-------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------------#
def temperature_and_humidity(channel):

    data = []  # 温湿度值
    j = 0  # 计数器

    time.sleep(1)  # 时延一秒

    GPIO.setup(channel_1, GPIO.OUT)

    GPIO.output(channel_1, GPIO.LOW)
    time.sleep(0.02)  # 给信号提示传感器开始工作

    GPIO.output(channel_1, GPIO.HIGH)
    GPIO.setup(channel_1, GPIO.IN)

    while GPIO.input(channel_1) == GPIO.LOW:
        continue

    while GPIO.input(channel_1) == GPIO.HIGH:
        continue

    while j < 40:
        k = 0
        while GPIO.input(channel_1) == GPIO.LOW:
            continue

        while GPIO.input(channel_1) == GPIO.HIGH:
            k += 1
            if k > 100:
                break

        if k < 8:
            data.append(0)
        else:
            data.append(1)

        j += 1

    # print ("sensor is working.")
    # print (data)			#输出初始数据高低电平

    humidity_bit = data[0:8]  # 分组
    humidity_point_bit = data[8:16]
    temperature_bit = data[16:24]
    temperature_point_bit = data[24:32]
    check_bit = data[32:40]

    humidity = 0
    humidity_point = 0
    temperature = 0
    temperature_point = 0
    check = 0

    for i in range(8):
        humidity += humidity_bit[i] * 2 ** (7 - i)  # 转换成十进制数据
        humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
        temperature += temperature_bit[i] * 2 ** (7 - i)
        temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
        check += check_bit[i] * 2 ** (7 - i)

    tmp = humidity + humidity_point + temperature + temperature_point  # 十进制的数据相加

    if check == tmp:  # 数据校验，相等则输出
        #print("temperature : ", temperature, ", humidity : ", humidity)
        time.sleep(0.2)
        return temperature, humidity
    
    #else:										
        #print ("wrong")
        #print ("temperature : ", temperature, ", humidity : " , humidity, " check : ", check, " tmp : ", tmp)   #错误输出错误信息，和校验数据
        
        

    #Remember to add "time.sleep(0.5)" while  you finish using it.
#-------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------------#
def soil_moisture_Rx():
    data = 0
    if ser.isOpen == False:
        ser.open()  # 打开串口
    # ser.write(b"Raspberry pi is ready")
    size = 2                       #ser.inWaiting()  # 获得缓冲区字符
    
    if size != 0:
        response = ser.read(size)  # 读取内容并显示
        data = int(response)
        ser.flushInput()  # 清空接收缓存区
        time.sleep(0.1)  # 软件延时
    
    return data
#-------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------------#
def motor_output(channel):

    #data = soil_moisture_Rx()

    if soil_moisture_Rx() < 10:

        for i in range(4):
            GPIO.output(channel_2, GPIO.LOW)
            time.sleep(1)
            GPIO.output(channel_2, GPIO.HIGH)
            time.sleep(1)

    else:
        GPIO.output(channel_2, GPIO.HIGH)
        time.sleep(0.1)
#-------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    
    try:
        while True:
            data_1 = temperature_and_humidity(channel_1)
            print(data_1)
            time.sleep(0.1)
            data_2 = soil_moisture_Rx()
            print(data_2)
            time.sleep(0.1)
            #motor_output(channel_2)
            #time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    ser.close()
    GPIO.cleanup()

