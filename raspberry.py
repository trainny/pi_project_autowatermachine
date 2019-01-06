from socket import *
import threading
import struct
import time
import cv2
import numpy

class Carame_Accept_Object:
    def __init__(self,S_addr_port=("",8888)):
        self.resolution=(640,480)
        self.img_fps=15
        self.addr_port=S_addr_port
        self.Set_Socket(self.addr_port)

    def Set_Socket(self,S_addr_port):
        self.server=socket(AF_INET,SOCK_STREAM)
        self.server.bind(S_addr_port)
        self.server.listen(5)
        
def check_option(object,client):
    info=struct.unpack('lhh',client.recv(8))
    if info[0]>888:
        object.img_fps=int(info[0])-888
        object.resolution=list(object.resolution)

        object.resolution[0]=info[1]
        object.resolution[1]=info[2]
        object.resolution = tuple(object.resolution)
        return 1
    else:
        return 0

def RT_Image(object,client,D_addr):
    if(check_option(object,client)==0):
        return
    camera=cv2.VideoCapture(0)
    img_param=[int(cv2.IMWRITE_JPEG_QUALITY),object.img_fps]
    i = 0
    while True:
        time.sleep(0.1)
        _,object.img=camera.read()
        object.img=cv2.resize(object.img,object.resolution)
        _,img_encode=cv2.imencode('.jpg',object.img,img_param)
        img_code=numpy.array(img_encode)
        object.img_data=img_code.tostring()
        try:
            client.send(struct.pack("lhh",len(object.img_data),object.resolution[0],object.resolution[1])+object.img_data)
        except:
            client.close()
            camera.release()
            break

if __name__ == '__main__':
    camera=Carame_Accept_Object()
    while True:
        client,D_addr=camera.server.accept()
        print("connect from:" , D_addr)
        print("---------------------------------------------------")
        threading.Thread(None,target=RT_Image,args=(camera,client,D_addr,)).start()
