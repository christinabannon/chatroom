# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from thread import *

# The first argument AF_INET is the address domain of the 
# socket. This is used when we have an Internet Domain with 
# any two hosts The second argument is the type of socket. 
# SOCK_STREAM means that data or characters are read in 
# a continuous flow.
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
IP_address = '127.0.0.1'
Port = 65433

# binds the server to an entered IP address and at the 
# specified port number. 
server.bind((IP_address, Port)) 

# listens for 100 active connections. This number can be 
# increased as per convenience. 
server.listen(100) 

list_of_client_connections = [] 
list_of_client_user_names = []
user_name = ""
quit_code = "QUIT!!!"
server_input = ""

print("Chatroom starting!")

def clientthread(connection, IP_address): 
	user_name = add(connection, IP_address)
	while True: 
		print("in clientthread")
		try: 
			message = connection.recv(2048) 
			print(message)
			if message.strip() == quit_code:
				remove(connection, user_name)
			elif message: 
				print("< " + user_name + " > " + message)
				message_to_send = "< " + user_name + " > " + message 
				broadcast(connection, message_to_send) 
			else: 
			# remove the connection
				remove(connection, user_name)

			if server_input == quit_code: 
				break
		except: 
			continue
	print("\n Broke out of clientthread while")

# Using the below function, we broadcast the message to all 
# clients who's object is not the same as the one sending 
# the message 
def broadcast(connection, message): 
	for client_connection in list_of_client_connections: 
		if client_connection!=connection: 
			try: 
				client_connection.send(message) 
			except: 
				# if the link is broken, we remove the client 
				remove(connection, user_name)

# When a new connection is added, send welcome to them, and inform everyone else 
# that they have arrived. 
def add(connection, IP_address):
	connection.send("<< Welcome to the chatroom! >>\n") 
	potential_user_name = connection.recv(2048)
	i = 0
	for already_taken_user_name in list_of_client_user_names: 
		while potential_user_name + "#" + str(i) == already_taken_user_name: 
			i = i + 1
	user_name = potential_user_name + "#" + str(i)
	connection.send("<< Your user name is " + user_name + " >>\n")
	connection.send("<< At any time type 'QUIT!!!' to exit >>\n")
	list_of_client_user_names.append(user_name)
	for client_connection in list_of_client_connections:
		if client_connection != connection: 
			client_connection.send(" << " + user_name + " has entered the chat... >> ")
	print("New connection # "+ str(len(list_of_client_connections)))
	print("   IP   : " + IP_address[0])
	print("   Name : " + user_name)
	return user_name

# Takes connection out of list of connections, 
# prints to server that they have left
# sends the exit code back to the client  
# broadcasts that the user left to all the other clients
def remove(connection, user_name): 
	if connection in list_of_client_connections: 
		list_of_client_connections.remove(connection) 
	exit_message = (" << " + user_name  + " has left the chat... >> ")
	connection.send(quit_code)
	print("... sent quit code from server to client")
	broadcast(connection, exit_message)
	connection.close()
	print("... closed connection with client")
	print(exit_message)

def end_chat():
	for connection in list_of_client_connections: 
		connection.send("<< Server is ending the chat. >> ")
		print("send << Server is ending the chat. >>")
		connection.send(quit_code)
		print("send quit code")
		connection.close()
		print("closed connection")
	print("<< Chat ending... >>")
	server.close()
	sys.exit()

threadNum = 0
while server_input == "" or not server_input: 
	print("In outer loop")
	# Accepts a connection request and stores two parameters, 
	# conn which is a socket object for that user, and addr 
	# which contains the IP address of the client that just 
	# connected
	connection, IP_address = server.accept() 

	# # prints t	he address of the user that just connected 
	# print(name + " connected")

	# Maintains a list of clients for ease of broadcasting 
	# a message to all available people in the chatroom
	list_of_client_connections.append(connection) 

	# creates an individual thread for every user 
	# that connects 
	thread.start_new_thread(clientthread,(connection,IP_address))
	print("Thread # " + str(threadNum))
	threadNum = threadNum + 1

print("Broke out of outerloop")
connection.close() 
server.close() 
