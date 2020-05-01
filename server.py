import socket
import threading
import Queue

# kill $(jobs -p) 

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print("Starting up chat room server")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
client_addresses = []
client_user_names = []
# received_packets = Queue.Queue()

# def receive_data(): 

#     received_packets.put((data, addr))

def process_data(): 
    data, addr = sock.recvfrom(2048)
    if addr in client_addresses:
        print("address recognized")
        user_name = client_user_names[client_addresses.index(addr)]
        data = "<" + user_name + ">" + data
        print(data)
        for address in client_addresses: 
            if addr[1] != address[1]: 
                sock.sendto(data, address)
                print("   sent " + data + " to  " 
                + client_user_names[client_addresses.index(address)])
    else: 
        add(data, addr)

    
def add(data, addr): 
    potential_user_name = data
    i = 0
    for already_taken_user_name in client_user_names: 
    	while potential_user_name + "#" + str(i) == already_taken_user_name: 
			i = i + 1
    user_name = potential_user_name + "#" + str(i)
    sock.sendto("<< Welcome to the chatroom! >>\n<< Your user name is " 
        + user_name + " >>\n<< At any time type 'QUIT!!!' to exit >>\n", 
        addr)
    client_addresses.append(addr)
    client_user_names.append(user_name)
    print("new address : " + str(addr) + "  " + user_name)

while True: 
    # receive_data()
    process_data()

# while True: 
#     data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#     print("received message: " + data)

client_addresses = []
client_user_names = []
sock.close()