import socket
from threading import Thread
import threading
import sys
import time
import struct
import os
from datetime import datetime
import pickle


UDPsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDP_PORT=7014

Clients_dic={}

bad_words = ["PORN", "SEX", "NAKED"]
db={}


client_server= open(r'\\.\pipe\data', 'r+b', 0)

lock=threading.Semaphore(1)
lock2=threading.Semaphore(1)


def handler(clientsock,addr):
    global Clients_dic, bad_words, client_server, UDP_PORT, UDPsock, lock
    global lock2, db

    while True:
        data=clientsock.recv(2048)
        print "recv: "+data
        #Clients_dic[data.split(",")[0]]=addr

        for w in bad_words:
                if w in data:
                    lock.acquire(1)
                    UDPsock.sendto("WARN", (addr[0],UDP_PORT))
                    lock.release()
                    date=str(datetime.now())
                    name=socket.gethostname()
                    if name in db:
                        db[name]=db[name]+[date]
                    else:
                        db[name]=[date]
                    data=""
                    for key in db:
                        data=data+";"+key+"%"
                        for var in db[key]:
                            data=data+var+","
                        data=data[:-1]
                    data=data[1:]
                    print data
                    lock2.acquire(1)
                    client_server.write(struct.pack('I', len(data)) + data)
                    client_server.seek(0)
                    lock2.release()

        
def Pipe_server_client():
    global UDPsock,Clients_dic
    print "function started"
    server_client = open(r'\\.\pipe\Orders', 'r+b',0)
    print "OPENED"

    #buffer = os.read(io, BUFFER_SIZE)
    while True:
        print "#waiting for data"
        n = struct.unpack('I', server_client.read(4))[0]    # Read str length
        Data = server_client.read(n)                           # Read str
        server_client.seek(0)
        print Data







    


    
def connecting():
    global HOST,PORT,Stop
    ADDR = ("0.0.0.0",8064)
    serversock = socket.socket()
    serversock.bind(ADDR)
    serversock.listen(15)
    while 1:
        print 'waiting for connection...'
        (clientsock_Reciving, addr) = serversock.accept()

        print '...connected from:', addr,' For Sending Info'
        t1 = Thread(target=handler, args=(clientsock_Reciving,addr,))
        t1.start()




        
if __name__=='__main__':

    Pipe_server_client_Thread = Thread(target=Pipe_server_client)
    Pipe_server_client_Thread.start()
    t =Thread(target=connecting) 
    t.start()
    
    
    
    
    
    
