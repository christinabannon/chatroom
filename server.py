import socket
import threading


# kill $(jobs -p) 

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print("Starting up chat room server")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
client_addresses = []
client_user_names = []
user_names_past = []

def process_data(): 
    data, addr = sock.recvfrom(2048)
    if addr in client_addresses:
        if data == "QUIT!!!": 
            remove(addr)
        else : 
            user_name = client_user_names[client_addresses.index(addr)]
            data = "<" + user_name + ">" + data
            broadcast(data, addr)
    else: 
        add(data, addr)

def broadcast(data, addr):
    print(data)
    for address in client_addresses: 
        if addr[1] != address[1]: 
            sock.sendto(data, address)

def add(data, addr): 
    user_name = make_username(data, addr)
    sock.sendto("<< Welcome to the chatroom! >>\n<< Your user name is " 
        + user_name + " >>\n<< At any time type 'QUIT!!!' to exit >>", 
        addr)
    client_addresses.append(addr)
    client_user_names.append(user_name)
    print("new address : " + str(addr) + "  " + user_name)
    intro_message = "<< " + user_name + " has entered the chat. >>"
    broadcast(intro_message, addr)

def make_username(data, addr):
    potential_user_name = data
    user_name = potential_user_name + "#" + str(addr[1]) + "#" + str(addr[0]) 
    return user_name

def remove(addr): 
    user_name = client_user_names[client_addresses.index(addr)]
    client_addresses.remove(addr)
    client_user_names.remove(user_name)
    user_names_past.append(user_name)
    exit_message = "<< " + user_name + " has left the chat. >>"
    broadcast(exit_message, addr)


while True: 
    process_data()

client_addresses = []
client_user_names = []
sock.close()