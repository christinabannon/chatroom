#Robert Reinhard
#05/01/2020
#This file is meant to host a server connection
import socket
import select
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

#creates the socket for the application
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#binds the server to the socket
server_socket.bind((IP, PORT))

#clients addresses
clients = []

while True:
    # receiving the data and address from datagram
    # buffer size 1024
    data, addr = server_socket.recvfrom(1024)
    # if its not a new client and they are on the list
    if addr in clients:
        print(data)
        for address in clients: 
            if addr != address: 
                server_socket.sendto(data, address)
    # if they are new and not on the list
    else: 
        clients.append(addr)
        user = data
        message = ("Welcome to the chat, " + user)
        print(message)
        for address in clients: 
            if addr != address:
                server_socket.sendto(message, address)





# #recieve messages
# def receive_message(client_socket):
#     try:

#         return{'header': message_header, 'data': client_socket.recv(message_length)}
    

#     except:
#         return False


# while True:
#     read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
#     for notified_socket in read_sockets:
#         if notified_socket == server_socket:
#             client_socket, client_address = server_socket.accept()

#             user = receive_message(client_socket)
#             if user is False:
#                 continue
#             sockets_list.append(client_socket)

#             clients[client_socket] = user

#             print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

#         else:
#             message = receive_message(notified_socket)

#             if message is False:
#                 print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
#                 sockets_list.remove(notified_socket)
#                 del clients[notified_socket]
#                 continue

#             user = clients[notified_socket]
#             print(f'Recieved message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

#             for client_socket in clients:
#                 if client_socket!= notified_socket:
#                     client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])



# for notified_socket in exceprion_sockets:
#     sockets_list.remove(notified_socket)
#     del clients[notified_socket]










