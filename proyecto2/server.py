import socket
import time

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
msgFromServer       = "SERVER"
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

def recive0():
    print("Servidor Disponible...")
    
    rcvpkt = UDPServerSocket.recvfrom(bufferSize)
    message = rcvpkt[0]
    address = rcvpkt[1]
    message = format(message)

    if(has_seq1(message)): 
        udt_send("1", address)
        recive0()

    time.sleep(3)
    print(message[4])

    return

def recive1():
    print("Servidor Disponible...")
    
    rcvpkt = UDPServerSocket.recvfrom(bufferSize)
    message = rcvpkt[0]
    address = rcvpkt[1]
    message = format(message)

    if(has_seq0(message)):
        udt_send("0", address)
        recive1()

    time.sleep(3)
    print(message[4])

    return

def has_seq1(rcvpkt):
    rcvpkt = rcvpkt[2]
    if(str(rcvpkt) == "1"): return True
    return False

def has_seq0(rcvpkt):
    rcvpkt = rcvpkt[2]
    if(str(rcvpkt) == "0"): return True
    return False

def udt_send(num, address):
    bytesToSend = str.encode(num)
    UDPServerSocket.sendto(bytesToSend, address)
    return


while(True):
    recive0()
    recive1()
