"""
-RANSOM-
Random functions and Types with various uses
MADE BY KHALVAAN aka kitsune
Licenzed by EXTREEME.corp [EXTREEME Foundation.ink]
"""
"""
P.S.: from modern me:
    This module consists mainly out of functions I didn't know there are other options to.
    So i wrote them myself.
    can't be bothered to rewrite this, so trash is what you get [be happy that some of the functions & classes even have documentation].
P.P.S.: from me reading this code:
    God, this code is horrible. I'm sorry for anyone who has to read this
"""

class Data:
    """Different Data Manipulation functions."""
    class string:
        """String Manipulation."""
        def strip(stringg:str,stripp:list|str) -> str:
            """Strips a string by the input [can also be a list]
            
            stringg = String you want to strip  [str]
            stripp = the characters you want to strip from stringg  [str, list]
            
            Returns: str"""
            if type(stripp)==list:
                word = stringg
                for x in stripp:
                    word = Data.string.strip(word,x)
                return word
            else:
                stripp = list(stripp)
                indx = 0
                ln = len(stripp)
                current = ""
                endstr = ""
                for x in stringg:
                    if x==stripp[indx]:
                        indx+=1
                        current+=x
                        if indx == ln:
                            current = ""
                            indx = 0
                    elif indx != 0:
                        indx=0
                        endstr+=current
                        current=""
                        endstr+=x
                    else:
                        endstr+=x
                        current=""
                return endstr
        
        def swap(string:str,swap:dict) -> str:
            """swaps specified characters [or strings] with others in the given string.
            
            string = str to swap  [str]
            swap = Characters you want to swap  [dict of chars or strings]
            
            Returns: str"""
            chgs = []
            for x in swap.keys():
                for y in range(len(string)):
                    if x == string[y:len(x)+y]:
                        chgs.append((y,swap[x],x))
            for x in chgs:
                strg = string[:x[0]]
                strg += x[1]
                strg += string[x[0]+len(x[2]):]
                string = strg
            return string
        def lines(string:str,endcharacter:str="\n",ignore_after:bool=False,include_endchar:bool=False) -> list:
            """splits a string into lines.
            
            string = input text or str [str]
            endcharacter = character to split after. [str]
            ignore_after = when true, will ignore everything that comes after the endcharacter until "\\n" is hit.
            Returns: list o' str"""
            lines = []
            curstr = ""
            readagn = True
            for x in string:
                if x == endcharacter:
                    lines.append(curstr)
                    curstr = ""
                if x == "\n" and ignore_after==True:
                    readagn = False
                if readagn:
                    curstr += x
            lines.append(curstr)
            return lines
    class Ransom_func:
        """Various Functions with little usecases"""
        def Dic_to_list(Dic:dict) ->list:
            """converts a Dict to a list with tuples (  {K1:V, K2:V} >>> [(K1,V),(K1,V)]  )
            
            Dic = input dictionary
            
            Returns: list(   [ ( Key, Value )]   )"""
            class twoident:
                def __init__(s,Key,Val):
                    s.Key = Key
                    s.Val = Val

            endlist = []
            for x in Dic:
                key = x
                Val = Dic[x]
                endlist.append(twoident(key,Val))#(key,Val))

            return endlist
"""
class IO:
    ""File and Directory Manipulation""
    class Files:
        ""File Manipulation (Helps with writing,Reading and editing of text files)""
        
"""
class Usefull_stuff:
    """Random stuff that doesnt fit all other classes"""
    def Ask(question,Answers,inv=False,failmsg="invalida answer! Try Again"):
        """Ask a Question to the user and check theyre input
        
        question = Question to be asked. [str]
        Answers = List of possible answers [List<str>]
        inv = return invalid answers (if False: will ask question again if false input.) [bool,def:False]
        failmsg = message to print out on fail (will be ignored if inv=False)

        returns: selected Answer e.x.:{"y","n"} [str]"""
        def _ask():
            global inp
            inp = input(f"{question}\t{str(Answers)}")
            if not inv and inp not in Answers:
                print(failmsg)
                _ask()
        _ask()
        return inp

    class Switch:
        """Switches between True or False with single functions [can be assigned a custom lenght {def out=bool,if btnlenght != None -> int} ]
        
        defstate = Creation State. [bool,int]
        btnlength = Length of the button {Button can be assigned a length}  [None,int]"""
        state=0
        trueval=0
        def __init__(s,defstate=False,btnlength=None):
            if btnlength == None:
                s.btnlength = "T"
                s.trueval = defstate
            elif type(btnlength) == int:
                s.btnlength = btnlength
                s.trueval = int(defstate)
            else:
                raise Exception("""btnlengt isn't an int or of type "None" """)
            if defstate == btnlength:
                s.state = True
            else:
                s.state = False
            
        def toggle(s,ammount = 1):
            """Switches switch (or raises it's value by the given ammount)"""
            if s.btnlength == "T":
                if s.state == True: s.state = False;s.trueval = 0
                else: s.state = True;s.trueval = 1
            else:
                s.trueval += ammount
                if s.trueval < 0:
                    s.trueval = 0
                if s.trueval == s.btnlength:
                    s.state = True
                elif s.trueval > s.btnlength:
                    s.state = False
                    s.trueval = 1
                else:
                    s.state = False
                
        def on(s,set):
            """Just sets the Switch to a value"""
            if type(s.state) == type(set):
                s.state = set
            else:
                raise Exception("""type of state and type of set isn't equal""")
    class PILTK_show:
        """This Class makes an Tkinter window to display PIL images without using show
        This should be used for applications with rapid display speeds for witch show
        is too inconvinient
        
        root = if there is already a Tkinter application running, Please input it here
        [CAUTION: This will close the window when the root closes] [Tkinter.Tk()]"""
        import tkinter
        from PIL import ImageTk, Image
        def __init__(s,root = None):
            if root == None:
                s.root = s.tkinter.Tk()
                s.uproot = None
            else:
                s.uproot = root
                s.root = s.tkinter.Toplevel(root)
            

            s.root.title("Pil tk img loader")
            refpic = s.Image.new("RGB",(100,100))
            s.tkimg = s.ImageTk.PhotoImage(refpic)
            s.pic = s.tkinter.Label(s.root,image = s.tkimg)
            s.pic.pack()

            s.exitFlag = False

            def on_quit():
                s.exitFlag = True
                s.root.destroy()
            s.root.protocol("WM_DELETE_WINDOW", on_quit)
            

            s.root.update()
        def show(s,img):
            """
            if s.exitFlag:
                return "WD_Destroyed"
            try: s.uproot.state()
            except: s.exitFlag = True;return "WD_Destroyed"
            """
            s.tkimg = s.ImageTk.PhotoImage(img)
            s.pic.config(image = s.tkimg)
            s.root.update()
    class Timer:
        """Easily count time and call functions using this class
        
        Start = Start the timer when class is initiated. [bool,False]"""
        import timeit
        def __init__(s,start=False):
            if start:
                s.start = s.timeit.default_timer()
        def time(s):
            return s.timeit.default_timer() - s.start
        def reset(s):
            s.start = s.timeit.default_timer()
        def timer(s,time):
            if s.timeit.default_timer() - s.start > time:
                return True
            else: return False
    def arg_dec(args=[],kwargs=[],Valargs={},Help="",return_null=2,overflow=0):
        """Function that helps sorting args and makes them acsessible
        args = list of available args

        kwargs = list of args (an dict with values appended is returned [string])

        Valargs = dict of args (args are directly formated into the right format) [type] [CAUTION::: This tries to convert string to the entered type,this wont work in most cases/output unexpected results[exept bool]]
        
        Help = define help to show and exit (can also be a dict with the arg and a short(1.liner) explanation [append "_end" to display a msg at the end])
        
        return_null = Will output all args that have not been specified with value null [0=False,1=True,2=output True False in normal args]
        
        overflow = Accepts x unspecified values and puts them in an list under "_emp" (0=deactivated)

        [CAUTION: make sure input arguments aren't inputted twice.(unexpected results may occour)]
        P.S: input Tulple with value for forced input (will return a message and exit when not specified ) [(value)]"""
        import sys

        comarg = sys.argv[1:]
        Allarg = args+kwargs
        ret_args = {}
        if return_null == 2:
            for x in args:
                ret_args[x] = False
            for x in kwargs:
                ret_args[x] = None
        elif return_null:
            for x in Allarg:
                ret_args[x] = None
        for x in Valargs.keys():
            Allarg.append(str(x))
            if return_null:
                ret_args[str(x)] = None
        if "_emp" in Allarg:
            raise Exception("cant assign _emp [Reserved for unspecified values]")
        for x in comarg:
            if x == "": pass
            elif x in ["-Help","-help","--Help","--help"]:
                if Help == "":
                    print("There seems to be no Help availible for this program...  );")
                elif type(Help) == dict:
                    print("\nAvailible options:")
                    nd = ""
                    for x in Help.keys():
                        if x == "_end":
                            nd = Help[x]
                        else:
                            print(f"\t{x} \t\t: {Help[x]}")
                    print(f"\t--help \t\t: Will Display this message and exit.\n{nd}\n")
                else:
                    print(Help)
                exit()
            elif x not in Allarg:
                print(f"Unknown option: \"{x}\"")
                print("Type -Help for Help")
                exit()
            elif x in args:
                ret_args[x] = True
            elif x in kwargs:
                try:
                    ret_args[x] = comarg[comarg.index(x)+1]
                    comarg[comarg.index(x)+1] = ""
                except:
                    print("Please input an valid operator after kword arg")
                    exit()
            elif x in Valargs.keys():
                if Valargs[x] == bool:
                    if comarg[comarg.index(x)+1] in ["True","true","t"]: ret_args[x] = True
                    elif comarg[comarg.index(x)+1] in ["False","false","f"]: ret_args[x] = False
                    else: print(f"option \"{comarg[comarg.index(x)]}\" can only be of type \"Bool\" (True/False)");exit()
                try:
                    ret_args[x]=Valargs[x](comarg[comarg.index(x)+1])
                except:
                    print(f"option \"{comarg[comarg.index(x)]}\" can only be of type \"{str(Valargs[x])}\"")
                    exit()
                try:
                    comarg[comarg.index(x)+1] = ""
                except:
                    print("Please input an valid operator after kword arg")
                    exit()
        return ret_args
class Types:
    """Usefull custom made Types for various usecases"""
    class Vector2:
        """A point on an 2d Surface defined by x and y.    [float]"""
        def __init__(s,x=0.0,y=0.0):
            s.x = x
            s.y = y
            s.Vector = (x,y)
        def __str__(s):
            return f"({s.x}, {s.y})"
        def __iter__(s):
            for x in range(2):
                yield s.Vector[x]
        def __getitem__(s,index):
            return s.Vector[index]
        def todict(s):
            return {"x":s.x,"y":s.y}
    class Vector3:
        """A point in an 3d Volume defined by x , y and z.    [float]"""
        def __init__(s,x=0.0,y=0.0,z=0.0):
            s.x = x
            s.y = y
            s.z = z
            s.Vector = (x,y,z)
        def __str__(s):
            return f"({s.x}, {s.y}, {s.z})"
        def __iter__(s):
            for x in range(3):
                yield s.Vector[x]
        def __getitem__(s,index):
            return s.Vector[index]

class networking:
    """Some various Networking Stuff"""
    class rec_snd_Server:
        """sets up an Networking server to send and recieve from chosen connection [CAUTION! Only works with similar server on the other side]
        
        [Has to be jet written.]
        """
        import socket
        import threading as thrd
        def __init__(s):
            s.socket = s.socket.socket()


#dec = Usefull_stuff.arg_dec(["-p"],["-path"],{"-open_WND":bool,"-ctm":int},{"-ctm":"Displays current path"})