#this code is a mess

import modules.HDMI_WRITE as HDMI_WRITE
import modules.recv_handler as recv_handler
import io
import numpy as np
from PIL import Image
import threading as thrd
from time import sleep
import logging
from datetime import datetime
#from Selfmade.Ransom import Usefull_stuff

curimg = b""
lastimg = b""
dispmes = (720,1280)

#sdr = "/home/pi/Programmz/Display/"
sdr = ""

def Disp_img():
    """Writes a PIL image (var img) to Framebuffer via modules.HDMI_WRITE"""
    global curimg
    Disp = HDMI_WRITE.Disp(dispmes[0],dispmes[1],4)
    #Disp = Usefull_stuff.PILTK_show()
    logging.info("Disp_img thread Loaded. (entering loop.)")
    while True:
        if curimg != b"":
            #logging.warning("Showing-pic")
            #Disp.show(curimg)
            #curimg = b""
            n = np.array(curimg)
            Disp.ShowArr(n)
            curimg = b""
        sleep(0.05)

if __name__ == "__main__":
    try:
        logging.basicConfig(filename="Log.txt",format='%(asctime)s,%(msecs)d\t%(name)s\t%(levelname)s\t%(message)s',datefmt='%H:%M:%S',level=logging.INFO)
        logging.info("Main Started.")
        #thread to recieve Picture Data from PC [modules.recv_handler]
        recv_H = thrd.Thread(target=recv_handler.conn,args=(("192.168.1.192",2223),),daemon=True)
        #thread to write recv't images to the Framebuffer of the device 
        Disper = thrd.Thread(target=Disp_img,daemon=True)
        recv_H.start();Disper.start()#start threads
        logging.info("Threads Started")
        # = HDMI_WRITE.Disp(dispmes[0],dispmes[1],4) #init Display with correct mesurements (&chanels)
        logging.info("Creating static Images")
        imgs = {"fg":Image.open(sdr+"Ransom/pic/fg1.png"),
                "bg":Image.open(sdr+"Ransom/pic/bg1.png"),
                "Splash":Image.open(sdr+"Ransom/pic/Splash.png"),
                "void":Image.new("RGBA",(dispmes[1],dispmes[0]),(0,0,0,255))}
        #Splash_Image=Image.Image.paste(Image.new("RGBA",(dispmes[1],dispmes[0]),(0,0,0,255)),imgs["Splash"].resize((dispmes[1],dispmes[0]))).convert("RGBA")
        Splash_Image=imgs["Splash"].resize((dispmes[1],dispmes[0])).convert("RGBA")
        lastimg=Splash_Image
        curimg = lastimg
        logging.info("Loading finished! entering Loop...")
        con_flag=False
        while True:
            if recv_handler.BT != b"":
                #logging.warning("lol1")
                showimg = Image.new('RGBA', (1280,720), (0,0,0,0))
                img = Image.open(io.BytesIO(recv_handler.BT))
                img = img.resize((dispmes[1],dispmes[0]))
                img.convert("RGBA")
                #img.save(f"{TRP}img.png")
                #lastimg.save(f"{TRP}lastimg.png")
                Image.Image.paste(lastimg,img,img)
                #lastimg.paste(img,lastimg.getbbox(),img)
                #lastimg.show()
                #input()
                #preimg.paste(img,(0,0),img)
                #showimg.paste(imgs["bg"],(0,0))
                #showimg.paste(img,(0,0),img)
                #showimg.paste(imgs["fg"],(0,0),imgs["fg"])
                #img = preimg.paste(img)
                
                curimg = lastimg
                recv_handler.BT = b""
                #logging.warning("lol2")
                recv_handler.rd=True
            elif recv_handler.LS_connection_status==False and con_flag == True:
                logging.warning("Lost Connection! Trying to reestablish")
                curimg = Splash_Image
                lastimg = imgs["void"]
                #lastimg = Splash_Image
                con_flag=False
            elif recv_handler.LS_connection_status==True and con_flag == False:
                logging.info("Connection reestablished!")
                curimg = Image.new("RGBA",(dispmes[1],dispmes[0]),(0,0,0,255))
                lastimg = Image.new("RGBA",(dispmes[1],dispmes[0]),(0,0,0,255))
                imgs["void"] = Image.new("RGBA",(dispmes[1],dispmes[0]),(0,0,0,255))
                con_flag=True
            sleep(0.05)
    except Exception as x:
        logging.exception(f"Critical error occured at {datetime.strftime('%d/%m/%Y %H:%M:%S')}.:\n\n",exc_info=True)
        logging.shutdown()
        exit()
        
else:
    logging.critical("Instance Allready running! closing second instance")
    logging.shutdown()
    exit()