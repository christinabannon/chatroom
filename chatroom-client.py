import socket
import select
import errno
import sys
import time
from thread import *

#Robert Reinhard
#05/01/2020
#This file is meant to host a client connection


#HEADER_LENGTH = 10;

IP = "127.0.0.1"
PORT = 1234

#take a username from the client
my_username = raw_input("Username: ")

#create the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(my_username, (IP, PORT))

def send():
    while True:
        input = raw_input("<" + my_username + ">")
        message = ("<" + my_username + ">" + input)
        if message:
            client_socket.sendto(message, (IP, PORT))

def receive():
    while True:
        data, addr = client_socket.recvfrom(1024)
        print(data)
    
start_new_thread(send, ())
start_new_thread(receive, ())

while True:
    time.sleep(1)

    


















