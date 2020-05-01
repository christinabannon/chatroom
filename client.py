import socket
import Queue
import sys
import os
from thread import * 
import time


UDP_IP = "127.0.0.1"
UDP_PORT = 5005
# MESSAGE = "Hello World!"
# print("UDP target IP:" + UDP_IP)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
# received_packets = Queue.Queue()

print("Enter your name")
name = sys.stdin.readline().strip()
sock.sendto(name, (UDP_IP, UDP_PORT))


def receive_data(): 
    while True: 
        data, addr = sock.recvfrom(2048)
        print(data)

def send_message(): 
    while True: 
        try: 
            message = sys.stdin.readline()
            if message != "qqq" : 
                sock.sendto(message, (UDP_IP, UDP_PORT))
                print("      sent!")
            else : 
                print("      did read qqq")
                sock.close()
                os._exit(1)
            sys.stdin.flush()
        except: 
            break

start_new_thread(send_message, ())
start_new_thread(receive_data, ())

try: 
    while 1: 
        time.sleep(0.01)
except KeyboardInterrupt: 
    print("\n<<< bye >>>")
    message = "QUIT!!!"
    sock.sendto(message, (UDP_IP, UDP_PORT))