import socket
import sys
import os
from thread import * 
import time


UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# first message to server contains the name
print("< Enter your name to join the chat! > ")
name = sys.stdin.readline().strip()
sock.sendto(name, (UDP_IP, UDP_PORT))

# receives data from server and prints it to chat
def receive_data(): 
    while True: 
        data, addr = sock.recvfrom(2048)
        print(data)

# sends the chat message to the server
def send_message(): 
    while True: 
        try: 
            message = sys.stdin.readline()
            if message:  
                sock.sendto(message, (UDP_IP, UDP_PORT))
                print("< You > " + message)
            sys.stdin.flush()
        except: 
            break

def exit_chat(): 
    print("\n<<< bye >>>")
    message = "QUIT!!!"
    sock.sendto(message, (UDP_IP, UDP_PORT))

start_new_thread(send_message, ())
start_new_thread(receive_data, ())

try: 
    while 1: 
        time.sleep(0.01)
except KeyboardInterrupt: 
    exit_chat()