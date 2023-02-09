import numpy as np


class Disp:
    def __init__(s,height,width,chanels):
        s.h,s.w,s.c = height,width,chanels
        s.height,s.width,s.chanels = height,width,chanels
        s.fb = np.memmap("/dev/fb0",dtype="uint8",mode="w+",shape=(s.h,s.w,s.c))
    def ShowImage(s,IMG):
        IMG = IMG.convert("RGBA")
        IMG = IMG.resize((s.w,s.h))
        n = np.array(IMG)
        n[:,:,[0,2]] = n[:,:,[2,0]]
        s.fb[:] = n
    def showBytes(s,bytesarr):
        n = np.ndarray(bytesarr)
        n[:,:,[0,2]] = n[:,:,[2,0]]
        s.fb[:] = n
    def ShowArr(s,numpyarr):
        n = numpyarr
        n[:,:,[0,2]] = n[:,:,[2,0]]
        s.fb[:] = n
