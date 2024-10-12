#Display whatever
#	made by KHALVAAN aka kitsune
# NOTE:
#   Parts of this code are really old and have been written by me from 3 years ago.
#	I don't take any responsebility for anything here, if you run this then any problems are your responebility
#	The code is also extreemly ugly.

import io
import logging
import Ransom.modules.Selfmade.Ransom as SRand



# Decodes arg input.
args = SRand.Usefull_stuff.arg_dec(args=["--debug_mode"],Valargs={"--style":""})

#args["--debug_mode"]=True # OVERRIDE #AV: why is this here?
debug_level=logging.INFO

if args["--debug_mode"]:
	logging.basicConfig(format='%(asctime)s,%(msecs)d\t%(name)s\t%(levelname)s\t%(message)s',datefmt='%H:%M:%S',level=debug_level)
else:
	logging.basicConfig(filename="Ransom/Log.txt",filemode='w+',format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',datefmt='%H:%M:%S',level=debug_level)

def log(msg:str,basename:str="main",tbs:int=5):
	# This Function is so dumb. I have no idea why i wrote this
	_f = '\t'*tbs
	return f"{basename}{_f}{msg}"

logging.info(log("Program Started Started!","main",5))


logging.info(log("Starting Main imports","main",5))
from time import sleep
#from pynotifier import Notification
#import threading as thrd
#import Ransom.modules.notify_serv as notify_serv
from PIL import Image,ImageDraw,ImageFont,ImageChops#,ImageTk
#import psutil
#import GPUtil
from os import listdir
import json
import socket
from datetime import datetime
import os
from importlib import import_module
from inspect import isfunction,isbuiltin
#import numpy as np
logging.info(log("main imports finnished!","main",5))

if __name__ == "__main__":

	######################################################## This is a remenent from when i had notification for this stuff.

	#ntThrd = notify_serv.start_thread()
	#ptr = thrd.Thread(target=notify_serv._initalize,daemon=True)


	#while True:
	#	print(notify_serv.notifications)
	#	sleep(2)
	"""
	Notification(
		title='Display Service Started.',
		description='Connection to the Display has been established',
		icon_path='--REDACTED--', # On Windows .ico is required, on Linux - .png
		duration=5,                                   # Duration in seconds
		urgency='normal',
		app_name="Display-Service"
	).send()
	"""

	########################################################

	try:
		logging.info(log("loading config...",tbs=5))
		config={}
		try:
			with open("Ransom/settings.json","r") as c:
				config=json.load(c)
		except FileNotFoundError:
			logging.critical(f"settings.json missing [{__file__}]\nHALTING PROGRAM")
			logging.shutdown()
			exit()
		except json.decoder.JSONDecodeError:
			logging.critical("Setting.json corrupt\nHALTING PROGRAM")
			logging.shutdown()
			exit()
		

		selected=config["various"]["style"]
		styles={}

		stl={}

		class insetfunc:
			"""Creates an instance for calleble inserts (for the "renderer")"""
			failed:bool=False # has the function failed to execute in the past?
			def __init__(s,func:callable,errfunc:callable,id:int) -> None:
				s.func:callable=func
				s.errfunc:callable=errfunc
				s.id:int=id
			def __call__(s,frame:int,faillist:dict={}) -> any:
				try:
					return s.func(id,frame)
				except Exception as D:
					if not s.failed:
						s.failed=True
						for x in range(len(faillist["items"])):
							if faillist["items"][x]["type"] == "errormsg":
								faillist["items"][x]["text"] += str(f"function \"{str(s)}\" failed at frame {frame}\n")
						logging.critical(f"Error in script: {str(D)}")
					return s.errfunc(str(s))
			def __str__(s):
				return s.func.__name__

		def load_styles():
			pth="Ransom/styles/"
			stldirs = listdir("Ransom/styles")
			for x in stldirs: # Work for later: only load the selected style & not all in the directory
				try:		  # P.S.: I don't feel like commenting this
					erload=False
					logging.info(log(f"loading style: {x}","main",5))
					with open(pth+x+"/style.json","r") as s:
						hdt = json.load(s)
						hdt["path"]=pth+x+"/"
						for y in hdt["pics"].keys():
							hdt["pics"][y] = Image.open(hdt["path"]+hdt["pics"][y])
						
						for y in hdt["fonts"].values():
							if not os.path.isfile(f"Ransom/styles/{x}/{y}"):
								logging.warning(log(f"Font \"{y}\" does not exist on specified location."))
								erload=True

						def rep_ident(inp:str,gve_id:int):
							fnd=0
							curcom=""
							argvs=[]
							inptxt=inp
							_t=0
							txt=[""]# string, lambda func, string
							#for z in hdt["items"][y]["text"]:
							for z in range(len(inptxt)):
								if inptxt[z:z+2] == "{%" and not fnd:
									fnd=1
								elif inptxt[z:z+2] == "%}" and fnd:
									fnd=0
									stylefuncmod = import_module(f"Ransom.styles.{x}.functions").call_func
									stylefunc = getattr(stylefuncmod,curcom[1:])
									errfunc = getattr(stylefuncmod,"__error__")
									#lf=4
									if "id" in hdt["items"][gve_id]:
										lf=hdt["items"][gve_id]["id"]
									else:
										lf=gve_id
									txt.append(insetfunc(stylefunc,errfunc,lf))
									#txt.append(lambda call,id=lf:stylefunc(id,call))
									txt.append("")
									_t=1
								elif fnd:
									curcom+=inptxt[z]
								elif _t==0:
									txt[-1]+=inptxt[z]
								else:
									_t=0
							for z in txt:
								if z == "":
									txt.remove("")
							
							if len(txt) == 0:
								txt = ""
							return txt

						for y in range(len(hdt["items"])):
							kdt = hdt["items"][y].keys()
							if "text" in kdt:
								#print(hdt["items"][y]["text"])
								hdt["items"][y]["text"] = rep_ident(hdt["items"][y]["text"],y)
								


							if type(hdt["items"][y]["xy"]) == str:
								hdt["items"][y]["xy"] = rep_ident(hdt["items"][y]["xy"],y)[0]
							else:
								hdt["items"][y]["xy"] = tuple(hdt["items"][y]["xy"])
							if "color" in kdt:
								if type(hdt["items"][y]["color"]) == str:
									hdt["items"][y]["color"] = rep_ident(hdt["items"][y]["color"],y)[0]
								else:
									hdt["items"][y]["color"] = tuple(hdt["items"][y]["color"])
							if "font" in kdt:
								if hdt["items"][y]["font"][0] not in hdt["fonts"].keys():
									logging.warning(log(f"Font \"{y}\" is not loaded [fonts have to be added to \"fonts\" section before use]"))
									erload=True
							if "pic" in kdt:
								hdt["items"][y]["pic"] = rep_ident(hdt["items"][y]["pic"],y)[0]
							if "deg" in kdt:
								if type(hdt["items"][y]["deg"]) == str:
									hdt["items"][y]["deg"] = rep_ident(hdt["items"][y]["deg"],y)[0]
								else:
									hdt["items"][y]["deg"] = tuple(hdt["items"][y]["deg"])
						
#{"type":"form","form":"box","xy":[1065,890],"size":[50,50],"color":[255,200,50],"border":[50,100,255]},
#{"type":"img","xy":[0,0],"pic":"{%anim%}","scale":1},
#{"type":"text","xy":"{%mv%}","text":"lol","color":"{%rainbow%}","font":["Norm",25]},
#{"type":"text","xy":[580,10],"text":"Display","color":"{%rainbow%}","font":["Norm",25]},
#{"type":"text","xy":[0,0],"text":"fps:{%frame%}","color":"{%rainbow%}","font":["Norm",60]},
#json-dump



						if not erload:
							styles[hdt["info"]["name"]]=hdt

				except FileNotFoundError:
					logging.warning(log(f"critical files missing in style \"{x}\"","main",5),exc_info=True)
				except json.decoder.JSONDecodeError:
					logging.warning(log(f"style.json file of \"{x}\" corrupt. please repair or replace.","main",5))
				except:
					logging.warning(log(f"loading style \"{x}\" failed","main",5),exc_info=True)
	
		logging.info(log("loading styles","main",5))
		load_styles()
		if selected not in styles.keys():
			logging.warning(log(f"style \"{selected}\" has either faild loading or doesn't exist. Reverting to \"default style\"","main",5))
			#print(styles)
			if "default Style" not in styles.keys():
				logging.critical(log(f"Couldn't revert back to default style because it is missing or has failed loading.\nHALTING PROGRAM","main",5))
				logging.shutdown()
				exit()
			selected="default Style"
		logging.info(log(f"style \"{selected}\" selected and successfully loaded.","main",5))
		stl=styles[selected]

		_fonts={}
		def get_font(font:str,font_size:int):
			"""Loads fonts as they are needed. [Reconizes preused fonts and imediatly returns them]"""
			global _fonts
			if (font,font_size) in _fonts.keys():
				return _fonts[(font,font_size)]
			else:
				logging.info(log(f"loading \"{font}\", {font_size}","main",5))
				_fonts[(font,font_size)]=ImageFont.truetype(stl["path"]+stl["fonts"][font],font_size) # error correction?
				#_fonts[(font,font_size)]=ImageFont.load_default()
				return _fonts[(font,font_size)]


		#NETWORK connect
		def connecttoraspi():
			try:
				host=(config["connection"]["host-ip"],config["connection"]["host-port"])
				conadddr=(config["connection"]["client-ip"],config["connection"]["client-port"])
				
				h_name = socket.gethostname()
				IP_addres = socket.gethostbyname(h_name)
				logging.info(log(f"Binding Socket to {host[0]} with port: {host[1]}"))
				s=socket.socket()
				_temp=0
				while(1):
					try:
						s.bind(host)
						break
					except OSError:
						if not _temp:
							logging.info(log("Waiting for network to open..."));_temp=1
						sleep(2)
				del _temp
				logging.info(log("bound socket."))
				logging.info(log(f"trying to connect to {conadddr}..."))
				tryvar=0
				while True:
					try:
						s.connect(conadddr)
						logging.info(log("connection succesful"))
						break
					except:
						if config["connection"]["retries"] <= tryvar and config["connection"]["retries"] != 0:
							logging.critical(f"couldn't connect to display raspi. Make sure correct adress and port are in the config file! Attemts:{tryvar}")
							logging.shutdown()
							exit()
						logging.warning(log(f"Connection timed out. Attemt:{tryvar}"))
						sleep(4)
						tryvar+=1
				return s
			except ConnectionRefusedError:
				logging.error("connection refused")
				logging.shutdown()
				exit()
			
		#s=connecttoraspi()

		display=(config["client-settings"]["width"],config["client-settings"]["height"])
		
		#preimd = Image.new("RGBA",display,(0,0,0,0))
		logging.info(log("Basic setup complete. entering Main & rendering loop..."))

		frame=0

		def exe(funct,imd:ImageDraw):
			if isinstance(funct,insetfunc):
				funct = funct(frame,stl)
					
			return funct

		def RENDER():
			global frame
			#create drawing objects
			image = Image.new("RGBA",display,(0,0,0,0))
			imd = ImageDraw.Draw(image,"RGBA")
			for x in stl["items"]:
				v={}
				for y in x.keys():
					v[y]=exe(x[y],imd)
				tpe=v["type"]
				if tpe   == "img":
					_t = stl["pics"][v["pic"]]
					if v["scale"] != 1:
						_t = _t.resize((round(_t.width*v["scale"]),round(_t.height*v["scale"])))
					image.paste(_t,v["xy"],_t)
				elif tpe in ["text","errormsg"]:
					out=""
					for y in v["text"]:
						if type(y) == str:
							out+=y
						else:
							out+=y(frame)
					#print(v["xy"],out,v["color"],get_font(v["font"][0],v["font"][1]),tpe,sep="    ||    ")
					imd.text(v["xy"],out,v["color"],get_font(v["font"][0],v["font"][1]))
				elif tpe == "form":
					if v["form"] == "box":
						imd.rectangle((v["xy"]),tuple(v["size"])),v["color"],tuple(v["border"])
					elif v["form"] == "circ":
						rd=v["radius"]
						deg=v["deg"]
						pot=v["xy"]
						#imd.pieslice((x["xy"]),(rd,rd)),0,200,"#ffff33")
						imd.pieslice(((pot[0]-rd,pot[1]-rd),(rd+pot[0],rd+pot[1])),deg[0],deg[1],v["color"])
					#logging.warn(str(_t)+str(type(_t)))
					
				#elif tpe == "circ"
			frame+=1
			return image

		#disp = SRand.Usefull_stuff.PILTK_show()
		#disp2 = SRand.Usefull_stuff.PILTK_show(disp.root)
		
		last=Image.new("RGBA",display,(0,0,0,0))

		def imgDifRGBA(img1,img2):
			"""img1-img2=diff"""
			new = img1.load()
			old = img2.load()

			diff = Image.new("RGBA",display,(0,0,0,0))

			for x in range(display[0]):
				for y in range(display[1]):
					rgba1 = (r,g,b,a) = new[(x,y)]
					rgba2 = (r,g,b,a) = new[(x,y)]
					#diff[]
			
		msk = Image.new("RGBA",display,(0,0,0,0))

		ltd = Image.new("RGBA",display,(0,0,0,255))

		s=connecttoraspi()
		Tmr = SRand.Usefull_stuff.Timer()
		while True:
			Tmr.reset()
			#RENDER().show()
			ntd=RENDER()
			#disp.show(ntd)
			#continue
			last = ImageChops.difference(ntd,last)
			#last.show()
			#input()
			#ntd.show("aft:"+str(frame))
			#disp.show(RENDER())
			#last = imgDifRGBA(ntd,last)
			thresh = 0
			fn = lambda x : 255 if x > thresh else 0
			r = last.convert('L').point(fn, mode='1')
			r = Image.composite(ntd,msk,r)
			r=r.resize((int(display[0]/config["client-settings"]["compression-scaling"]),int(display[1]/config["client-settings"]["compression-scaling"])))

            #r.show()
			#ntd.show()
			#last.show()
			ltd.paste(r,(0,0),r)
			#ltd.show()


			#ltd.paste(r)
			#ltd.show()
			#disp.show(ltd)
			#disp2.show(r)
			last=ntd
			
			#--NETWORKING--

			#logging.info("lol1")

			buf = io.BytesIO()
			r.save(buf,format="png")
			b = buf.getvalue()
			datapacks=[]
			packsize=(1000,1000)
			packs= int(len(b)/packsize[1])
			datapacks.append(b[:packsize[0]])
			for x in range(packs):
				if x!=0:
					datapacks.append(b[packsize[0]*x:(packsize[0]*(x+1))])
			datapacks.append(b[packsize[0]*packs:])
			#logging.info(f"{len(datapacks)},{len(b)}")
			try:
				for x in datapacks:
					s.send(len(x).to_bytes(2,"little"))
					assert s.recv(10) == b"4"
					s.send(x)
					recv = s.recv(10) # recieve control signal
					if recv == b"1":
						pass
					elif recv == b"2":
						s.close()
						logging.info("connection closed by client.")
						logging.shutdown()
						exit()
					else:
						assert "unknown controll signal"==0
				s.send(b"2")
			except (TimeoutError,AssertionError): # reset the connection
				logging.warning(f"Timeout error / Invalid data recieved. resetting Connection...")
				s.close()
				s = connecttoraspi()
				last=Image.new("RGBA",display,(0,0,0,0))
				msk = Image.new("RGBA",display,(0,0,0,0))
				ltd = Image.new("RGBA",display,(0,0,0,255))
			except:
				s.close()
				logging.critical(f"Unexpected error occured...",exc_info=True)
				logging.shutdown()
				exit()
			#logging.info("lol3\n\n")
			
			#s.send(len(x).to_bytes(2,"little"))
			#assert s.recv(10) == b"4"
			#!!   RT == Render Time (how long each render SHOULD Take.)
			while True:
				if Tmr.time() >= config["host-settings"]["RT"]:
					break
				sleep(0.1)

			


			#--NETWORKING--

			#sleep(0.3)
			#input()
			#input()
		
		#  ANIM: scan all pics in animation directory, take name without .png and add it
		



		#input()
		#exit()
		#raise Exception("endoffile")
	except Exception as x:
		logging.exception(log(f"Critical error occured at {datetime.strftime('%d/%m/%Y %H:%M:%S')}.:\n\n","main",5),exc_info=True)
		logging.shutdown()
		exit()
else:
    logging.exception("Second Process Running...\nexiting...")
    logging.shutdown()
    exit()