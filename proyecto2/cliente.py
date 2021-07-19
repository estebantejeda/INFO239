# Basado en tdf2.2

import socket
import random
import time

msgFromClient       ="Esteban"
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def init(msg):
    count = len(msg)
    k = 0
    while(k < count):
        x = send0(msg[k])
        send1(x)
        k+=1
        x = send2(msg[k])
        send3(x)
        k+=1
    return

def send0(data):
    sndpkt = make_pkt(0, data)
    print("Enviando...")
    udt_send(sndpkt)
    return sndpkt

def send1(sndpkt):
    rcvpkt = UDPClientSocket.recvfrom(bufferSize)
    rcvpkt = "{}".format(rcvpkt[0])
    if(isACK(rcvpkt, 1)): 
        udt_send(sndpkt)
        send1(sndpkt)
    return

def send2(data):
    sndpkt = make_pkt(1, data)
    print("Enviando...")
    udt_send(sndpkt)
    return sndpkt

def send3(sndpkt):
    rcvpkt = UDPClientSocket.recvfrom(bufferSize)
    rcvpkt = "{}".format(rcvpkt[0])
    if(isACK(rcvpkt, 0)): 
        udt_send(sndpkt)
        send3(sndpkt)
    return

# Función que crea el paquete
def make_pkt(num, data):
    data = str(num)+"-"+data
    return str.encode(data)

# Función que envía el paquete al servidor
def udt_send(sndpkt):
    UDPClientSocket.sendto(sndpkt, serverAddressPort)
    return

def isACK(rcvpkt, num):
    rcvpkt = rcvpkt[2]
    num = str(num)
    if(rcvpkt == num): return True
    return False

init(msgFromClient)