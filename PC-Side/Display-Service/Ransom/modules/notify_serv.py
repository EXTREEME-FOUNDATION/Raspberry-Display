# This code is not up to date anymore, I'm keeping it tho just in case.
# Also this only runs on linux and is completely broken.

from logging import raiseExceptions
import subprocess
from time import sleep
import threading as thrd
import logging


def log(msg:str,basename,tbs=2):
	_f = '\t'*tbs
	return f"{basename}{_f}{msg}"


notifications=[]
class notification:
    def __init__(s,time:float,id:int=0):
        s.id = id
        s.time=time
        s.snd_name=""
        s.icon=""
        s.header=""
        s.content=""
        #s.urgency=""  #Unused (too complicated to decode)

    def __str__(s) -> str:
        return f"time: {str(s.time)}\nsender: {s.snd_name}\nicon_path/icon: {s.icon}\ntitle: {s.header}\nmessage: {s.content}"#\nurgency: {s.urgency}"


def _initalize():
    """The main subprocess method (call this directly with Threading.Thread)"""
    global _notifval,_flag,_flag_iter,_spec_flag,notifications

    _notifval=0
    _flag="null"
    _flag_iter=0
    _spec_flag=False

    _sbProc = subprocess.Popen(['dbus-monitor',"interface='org.freedesktop.Notifications'"],stderr=subprocess.PIPE, universal_newlines=True,stdout=subprocess.PIPE)
    
    logging.info(log("subproc has been created without error",__name__+":subproc",1))
    
    while True:
        ut = _sbProc.stdout.readline()
        if _flag == "null":
            if ut[:11] == "method call":
                tme=0
                for x in range(len(ut)):
                    #print(ut[x:x+6])
                    if ut[x:x+4] == "time":
                        tme=float(ut[x+5:x+5+17])
                    #print("#"+ut[x:x+6]+"#","#"+ut[x:x+4]+"#")
                    if ut[x:x+6] == "member":
                        v = ut[x+7:-1]
                        if v == "Notify":
                            ir = 0
                            if len(notifications) == 0: ir = _notifval
                            notifications.append(notification(tme,ir))
                            _flag="Notification"
            elif ut[:6] == "signal":
                for x in range(len(ut)):
                    if ut[x:x+6] == "member":
                        v = ut[x+7:-1]
                        #print(v)
                        if v == "NotificationClosed":
                            _flag="signal"
            #else:#trash
            #   print(ut[:-1])
        elif _flag == "Notification":
            if _flag_iter  ==  0: notifications[-1].snd_name= ut[11:-2]
            elif _flag_iter == 1: pass
            elif _flag_iter == 2: notifications[-1].icon= ut[11:-2]
            elif _flag_iter == 3: notifications[-1].header= ut[11:-2]
            elif _flag_iter == 4:
                #print("#"+ut+"#")
                if ut[11:-2] == "":
                    _flag_iter-=1
                    _spec_flag=True
                elif _spec_flag:
                    notifications[-1].content= ut[:-1]
                else:    
                    notifications[-1].content= ut[11:-1]
            elif _flag_iter >  4:
                #print(ut[3:3+5])
                if ut[3:3+5]== "int32":
                    _flag="null"
                    _flag_iter=0
                    _spec_flag=False
                    #print(str(notifications[-1]))
            if _flag != "null":
                _flag_iter += 1
        elif _flag=="signal":
            #print(ut)
            if _flag_iter == 0:
                xtr = ut[10:-1]
                if len(notifications) == 1:
                    #print("REMOVED: "+notifications[-1].snd_name)
                    notifications.remove(notifications[-1])
                    _notifval=str(int(xtr)+1)
                elif len(notifications) == 0:
                    _notifval=str(int(xtr)+1)


                for x in notifications:
                    if x.id == xtr:
                        #print("REMOVED: "+x.snd_name)
                        notifications.remove(x)
                        break


                _flag_iter+=1
            elif _flag_iter == 1:
                _flag_iter = 0
                _flag="null"
        #print(ut)
        #print(msg[:-1])

def start_thread():
    """Start the subprocess with this method
    
    returns Thread object. (this just sets up the thread and starts it. use _initalize if you want to run it directly)"""
    kfr = thrd.Thread(target=_initalize,daemon=True)
    kfr.start()
    logging.info(log("notify thread has been succesfully Started!",__name__))
    return kfr