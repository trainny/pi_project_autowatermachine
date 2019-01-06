from socket import *
import cv2
import threading
import struct
import numpy
import time
from tkinter import *
from PIL import Image
from PIL import ImageTk
import paho.mqtt.client as mqtt

class MQTT:
    def __init__(self):
        self.Host = "139.199.89.222"
        self.Port = 1883
        self.Client = mqtt.Client()
        self.Client.connect(self.Host,self.Port,60)

    def publish(self,Topic,Message):
        self.Client.publish(Topic,Message,qos=0,retain=False)

    def subcribe(self,Topic):
        self.Client.loop_start()
        self.Client.subscribe(Topic,1)
        self.Client.on_message = self.on_message_come

    def on_message_come(self,client,userdata,msg):
        self.msg_come = msg.payload.decode('gbk')[1:-1]
        self.AT_data.set("大气温度\n"+self.msg_come.split(',')[1]+"C\n")
        self.AH_data.set("大气湿度\n"+self.msg_come.split(',')[0]+"%\n")
        self.SH_data.set("土壤湿度\n"+self.msg_come.split(',')[2]+"%\n")

class Camera():
    def __init__(self):
        self.camera_cmd = 0
        
    def init(self):
        self.resolution=[640,480]
        self.addr_port=('192.168.137.238',8888)
        self.src=888+15
        self.interval=0
        self.img_fps=15
        self.client=socket(AF_INET, SOCK_STREAM)
        self.connect()

    def connect(self):
        while True:
            try:
                self.client.connect(self.addr_port)
                break
            except Exception:
                print("can't connect to the server")
                time.sleep(1)

    def Image(self):
        self.init()
        while self.camera_cmd:
            try:
                info=struct.unpack("lhh",self.client.recv(8))
                buf_size=info[0]
                if buf_size:
                    try:
                        self.buf=b""
                        temp_buf=self.buf
                        while(buf_size):
                            temp_buf=self.client.recv(buf_size)
                            buf_size-=len(temp_buf)
                            self.buf+=temp_buf
                            data = numpy.fromstring(self.buf, dtype='uint8')
                            self.image = cv2.imdecode(data, 1)
                            cv2.imshow("camera", self.image)
                    except:
                        pass
                    finally:
                        if(cv2.waitKey(10)==27):
                            self.camera_cmd = 0
                            self.client.close()
                            cv2.destroyAllWindows()
                            self.camera_v.set("打开视频")
                            self.btn_up.config(state = DISABLED)
                            self.btn_down.config(state = DISABLED)
                            self.btn_left.config(state = DISABLED)
                            self.btn_right.config(state = DISABLED)
                            break
            except:
                break
                    
    def thread_camera(self):
        if self.camera_v.get()=="打开视频":
            self.camera_v.set("关闭视频")
            self.btn_up.config(state = NORMAL)
            self.btn_down.config(state = NORMAL)
            self.btn_left.config(state = NORMAL)
            self.btn_right.config(state = NORMAL)
            self.camera_cmd = 1
            threading.Thread(target=self.Image).start()
        else:
            self.camera_cmd = 0
            cv2.destroyAllWindows()
            self.camera_v.set("打开视频")
            self.btn_up.config(state = DISABLED)
            self.btn_down.config(state = DISABLED)
            self.btn_left.config(state = DISABLED)
            self.btn_right.config(state = DISABLED)

    def control_up(self):
        MQTT.publish(self,"ding_water","up")

    def control_down(self):
        MQTT.publish(self,"ding_water","down")

    def control_left(self):
        MQTT.publish(self,"ding_water","left")

    def control_right(self):
        MQTT.publish(self,"ding_water","right")

    def control_water(self):
        MQTT.publish(self,"ding_water","water")

    def control_fertilizer(self):
        MQTT.publish(self,"ding_water","fertilizer")

class TK(Camera,MQTT):
    def __init__(self):
        MQTT.__init__(self)
        self.tk = Tk()
        self.tk.title("懒人实验小助手")
        self.frame_data = Frame(width=300,height=270,bg='white')
        self.frame_fertilizer = Frame(width=150,height=100,bg='white')
        self.frame_water = Frame(width=150,height=100,bg='white')
        self.frame_camera_switch = Frame(width=270,height=100,bg='blue')
        self.frame_camera_up = Frame(width=90,height=90,bg='blue')
        self.frame_camera_down = Frame(width=90,height=90,bg='blue')
        self.frame_camera_left = Frame(width=90,height=90,bg='blue')
        self.frame_camera_right = Frame(width=90,height=90,bg='blue')
        self.frame_data.grid(row=0,column=0,rowspan=3,columnspan=2,padx=0,pady=0)
        self.frame_fertilizer.grid(row=3,column=0,padx=2,pady=0)
        self.frame_water.grid(row=3,column=1,padx=2,pady=0)
        self.frame_camera_up.grid(row=0,column=3,padx=0,pady=0)
        self.frame_camera_left.grid(row=1,column=2,padx=0,pady=0)
        self.frame_camera_right.grid(row=1,column=4,padx=0,pady=0)
        self.frame_camera_down.grid(row=2,column=3,padx=0,pady=0)
        self.frame_camera_switch.grid(row=3,column=2,columnspan=3,padx=2,pady=5)
        self.frame_data.grid_propagate(0)
        self.frame_camera_switch.grid_propagate(0)
        self.AT_data = StringVar()
        self.AH_data = StringVar()
        self.SH_data = StringVar()
        self.AT_data.set("大气温度\n26C\n")
        self.AH_data.set("大气湿度\n60%\n")
        self.SH_data.set("土壤湿度\n70%\n")

    def btn(self,position,v,CMD,w,h):
        self.btn = Button(position,textvariable = v,command = CMD,width=w,height=h)
        self.btn.pack(fill="both", expand=True, padx=0, pady=0)

    def camera_switch(self):
        self.camera_v = StringVar()
        self.camera_v.set("打开视频")
        self.btn_up.config(state = DISABLED)
        self.btn_down.config(state = DISABLED)
        self.btn_left.config(state = DISABLED)
        self.btn_right.config(state = DISABLED)
        self.btn(self.frame_camera_switch,self.camera_v,self.thread_camera,37,4)

    def control(self):
        self.btn_up=Button(self.frame_camera_up,text = "↑",\
                           command = self.control_up,width=12,height=5)
        self.btn_up.pack(fill="both", expand=True, padx=0, pady=0)
        self.btn_down = Button(self.frame_camera_down,text = "↓",\
                               command = self.control_down,width=12,height=5)
        self.btn_down.pack(fill="both", expand=True, padx=0, pady=0)
        self.btn_left = Button(self.frame_camera_left,text = "←",\
               command = self.control_left,width=12,height=5)
        self.btn_left.pack(fill="both", expand=True, padx=0, pady=0)
        self.btn_right = Button(self.frame_camera_right,text = "→",\
                                command = self.control_right,width=12,height=5)
        self.btn_right.pack(fill="both", expand=True, padx=0, pady=0)

        self.btn_water = Button(self.frame_water,text = "浇水",\
                            command = self.control_water,width = 15,height = 4)
        self.btn_water.pack(fill="both", expand=True, padx=0, pady=0)
        self.btn_fertilizer = Button(self.frame_fertilizer,text = "施肥",
                        command = self.control_fertilizer,width = 15,height = 4)
        self.btn_fertilizer.pack(fill="both", expand=True, padx=0, pady=0)

    def data_show(self):
        self.AT = Label(self.frame_data,textvariable = self.AT_data,justify='left',\
                        width=28,height=3,wraplength=80,font = 50)
        self.AT.pack()
        self.AH = Label(self.frame_data,textvariable = self.AH_data,justify='left',\
                        width=28,height=3,wraplength=80,font = 50)
        self.AH.pack()
        self.SH = Label(self.frame_data,textvariable = self.SH_data,justify='left',\
                        width=28,height=3,wraplength=80,font = 50)
        self.SH.pack()
        
        
if __name__ == '__main__':
    tk = TK()
    tk.init()
    tk.client.close()
    tk.control()
    tk.camera_switch()
    tk.data_show()
    tk.subcribe("ding_water_pi")
    tk.tk.mainloop()
