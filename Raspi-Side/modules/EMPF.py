import HDMI_WRITE
import socket
import io
import numpy as np
from PIL import Image
import multiprocessing as mpr
from time import sleep
from ctypes import c_char_p as ch_str

defpath = "/home/pi/Desktop/PyTests/"


def conn(connect,BT):
    print(BT)
    s = socket.socket()

    s.bind(connect)
    s.listen(5)
    while True:
        try:
            c, v = s.accept()
            print("connected to ",v)
            NDFlag = False
            while True:
                b = b""
                while True:
                    red = c.recv(100)
                    if red == b"2":break
                    elif red == b"11":BT[1] = 1;break
                    elif red == b"12":BT[1] = 2;break
                    szs = int.from_bytes(red,"little")
                    c.send(b"4")
                    recv = c.recv(szs)
                    if recv == b"2":
                        break
                    c.send(b"1")
                    b += recv
                BT[0] = b
        except socket.error:
            print("End con")
            pass
        except Exception as e:
            print(e)
            exit()
def Arrcon(img):
    Disp = HDMI_WRITE.Disp(720,1280,4)
    while True:
        if img.value != b"":
            n = np.array(img.value)
            Disp.ShowArr(n)
            img.value = b""
        sleep(0.05)

if __name__ == "__main__":
    manager = mpr.Manager()
    subVar1 = manager.list([b"",1])
    subVar2 = manager.Value(ch_str,b"")
    sndpr = mpr.Process(target=conn,args=(("192.168.1.192",2223),subVar1,))
    arrai = mpr.Process(target=Arrcon,args=(subVar2,))
    sndpr.start()
    arrai.start()
    Disp = HDMI_WRITE.Disp(720,1280,4)
    imgs = {1:{"fg":Image.open(defpath+"pic/fg1.png"),"bg":Image.open(defpath+"pic/bg1.png")},2:{"fg":Image.open(defpath+"pic/fg2.png"),"bg":Image.open(defpath+"pic/bg2.png")}}
    preimg = Image.new('RGBA', (1280,720), (0,0,0,0))
    #sleep(5)
    while True:
        if subVar1[0] != b"":
            showimg = Image.new('RGBA', (1280,720), (0,0,0,0))
            img = Image.open(io.BytesIO(subVar1[0]))
            img = img.resize((Disp.width,Disp.height))
            img.convert("RGBA")
            Page = subVar1[1]
            #preimg.paste(img,(0,0),img)
            showimg.paste(imgs[Page]["bg"],(0,0))
            showimg.paste(img,(0,0),img)
            showimg.paste(imgs[Page]["fg"],(0,0),imgs[Page]["fg"])
            #img = preimg.paste(img)
            subVar2.value = showimg
            subVar1[0] = b""
        sleep(0.05)