from datetime import datetime
from math import sin,cos,tan
#from pickletools import read_uint1
from Selfmade.Ransom import Usefull_stuff
import psutil
import GPUtil

class ext_func:
    def perx(percent):
        return (percent[1],round((percent[2] - percent[1])*(percent[0]/100) + percent[1],0))
class call_func:
    ltp=0
    ekh=Usefull_stuff.Timer(True)
    fps=0
    lst=0
    refefe=20
    cgr=refefe
    lastest=[(0,0),(0,0),(0,0)]
    errorvals={
        "dt":"0:0:0 | 0.0.0",
        "cpu_usage":(0,0),
        "gpu_usage":(0,0),
        "ram_usage":(0,0)
    }
    def __error__(func_name:str) -> any:
        """Function for returning a default value if error in script occurs"""
        return call_func.errorvals.get(func_name,0)
    def dt(id,call) -> str:
        now = datetime.now()
        t = now.strftime("%H:%M:%S | %d.%m.%y")
        return t
    def cpu_usage(id,call) -> int:
        if call_func.cgr >= call_func.fps:
            call_func.lastest[0] = ext_func.perx((psutil.cpu_percent(),180+66,270+24))
        return call_func.lastest[0]
    def gpu_usage(id,call) -> int:
        if call_func.cgr >= call_func.fps:
            call_func.lastest[1] = ext_func.perx((GPUtil.getGPUs()[0].load*100,180+66,270+24))
        return call_func.lastest[1]
    def ram_usage(id,call) -> int:
        if call_func.cgr >= call_func.fps:
            call_func.lastest[2] = ext_func.perx((psutil.virtual_memory().percent,180+66,270+24))
            call_func.cgr=0
        call_func.cgr+=1
        return call_func.lastest[2]
    def frame(id,call) -> str:
        if call_func.ekh.timer(1):
            call_func.fps= call - call_func.lst
            call_func.lst=call
            call_func.ekh.reset()
        return str(call_func.fps)
    def rainbow(id,call):
        return (abs(round(255*sin(call*3))),abs(round(255*cos(call*0.5))),abs(round(255*tan(call*0.1))))
    def mv(id,call):
        #[1000,200]
        return (1000+100*sin(call*0.1),200+100*cos(call*0.1))
    def anim(id,call):
        call_func.ltp+=1
        if call_func.ltp >= 19:call_func.ltp=1
        return str(call_func.ltp)