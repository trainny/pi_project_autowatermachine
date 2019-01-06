# -*- coding: utf-8 -*
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200)
if ser.isOpen == False:
    ser.open()                # 打开串口
#ser.write(b"Raspberry pi is ready")
try:
    while True:
        size = ser.inWaiting()               # 获得缓冲区字符
        if size != 0:
            response = ser.read(size)        # 读取内容并显示
            data = int(response)
            #data = str(b, encoding = "utf-8")
            #data = bytes.decode(response)
            print(data)
            ser.flushInput()                 # 清空接收缓存区
            time.sleep(0.1)                  # 软件延时
            
except KeyboardInterrupt:
    ser.close()
