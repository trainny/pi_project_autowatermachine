#!/usr/bin/python
# -*- coding: UTF-8 -*-


import RPi.GPIO as GPIO
import serial
import time
#-------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------------#
channel_1 = 11			#引脚号11

ser = serial.Serial('/dev/ttyUSB0', 115200)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # 以BOARD编码格式

#-------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------------#
def get_value(channel):

    data = []  # 温湿度值
    
    j = 0  # 计数器
    
    moisture = 0
    humidity = 0
    humidity_point = 0
    temperature = 0
    temperature_point = 0
    check = 0
    
    
    if ser.isOpen == False:
        ser.open()  # 打开串口
     
    # ser.write(b"Raspberry pi is ready")
    size = 2    #ser.inWaiting()  # 获得缓冲区字符
    
    if size != 0:
        response = ser.read(size)  # 读取内容并显示
        moisture = int(response)
        ser.flushInput()  # 清空接收缓存区
        #time.sleep(0.1)  # 软件延时
    

    time.sleep(1)  # 时延一秒

    GPIO.setup(channel, GPIO.OUT)

    GPIO.output(channel, GPIO.LOW)
    time.sleep(0.02)  # 给信号提示传感器开始工作

    GPIO.output(channel, GPIO.HIGH)
    GPIO.setup(channel, GPIO.IN)

    while GPIO.input(channel) == GPIO.LOW:
        continue

    #while GPIO.input(channel) == GPIO.HIGH:
       # continue

    while j < 40:
        k = 0
        while GPIO.input(channel) == GPIO.LOW:
            continue

        while GPIO.input(channel) == GPIO.HIGH:
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
    
    for i in range(8):
        humidity += humidity_bit[i] * 2 ** (7 - i)  # 转换成十进制数据
        humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
        temperature += temperature_bit[i] * 2 ** (7 - i)
        temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
        check += check_bit[i] * 2 ** (7 - i)

    tmp = humidity + humidity_point + temperature + temperature_point  # 十进制的数据相加
    
    time.sleep(0.1)
    

    if check == tmp and humidity <= 95 and temperature <=50 and moisture <= 100:  # 数据校验，相等则输出
        #print("temperature : ", temperature, ", humidity : ", humidity)    
        return humidity,temperature,moisture
    
    else:
        return 0,0,moisture

#-------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    
    try:
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

