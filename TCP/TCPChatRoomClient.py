# Python program to implement client side of chat room. 
import socket 
import select 
import sys 

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

IP_address = '127.0.0.1'
Port = 65433
# server.connect((IP_address, Port)) 
print("Enter your name:")
name = sys.stdin.readline().strip()
server.sendto(name, IP_address, Port)

message = ""
quit_code = "QUIT!!!"

while message != quit_code: 
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
  
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            print(message) 
        else: 
            message = sys.stdin.readline() 
            server.send(message) 
            sys.stdout.write("< You >") 
            sys.stdout.write(message) 
            sys.stdout.flush() 
            if message == quit_code : 
                break

sys.exit()
