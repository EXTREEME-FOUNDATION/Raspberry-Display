import socket
from time import sleep
import logging
from time import sleep

BT=b"" # Bytes Bild
rd=True #stop recieving until Pic has been read
LS_connection_status=False #connection status
#opts={"option":99} Unused until further Development (see line with b"11")

def conn(connect):
    """conn Thread.
    connect: (HOST,PORT)
    
    recv's images from connected Hosts"""
    global BT
    global rd
    global LS_connection_status
    
    logging.info("recv thread started.")

    s = socket.socket()
    logging.info("binding adress...")
    tryy = 0
    while True:
        try:
            s.bind(connect)
            break
        except:
            tryy+=1
            logging.warning(f"Failed binding adress. attempt:{tryy}")
            sleep(1)
    logging.info(f"Bound Adress to {connect}.")
    logging.info("listening...")
    s.listen(5)
    while True:
        try:
            c, v = s.accept()
            logging.info(f"connected to {v}. Starting Transmission")
            NDFlag = False
            while True:
                if LS_connection_status==False:
                    LS_connection_status=True
                b = b""
                while rd != True:
                    sleep(0.01)
                while True:
                    red = c.recv(100)
                    if red == b"2":break
                    elif red == b"11":pass;break#BT = 1;break
                    elif red == b"12":pass;break#BT = 2;break
                    szs = int.from_bytes(red,"little")
                    c.send(b"4")
                    recv = c.recv(szs)
                    if recv == b"2":
                        break
                    c.send(b"1")
                    b += recv
                BT = b
                rd=False
        except socket.error as e: #Error mit socket (startet verbindung neu)
            logging.warning(f"Connection error... {e}")
            LS_connection_status = False
        except Exception as e: #Alles Andere (stopt application)
            logging.critical(f"Critical error in recv thread. {e}")
            exit()
