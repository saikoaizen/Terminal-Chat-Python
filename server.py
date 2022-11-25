import socket
import threading

#Creating a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Socket Binding Details
IP = ""
PORT = 0000

#Binding the socket to the specified IP Address
s.bind((IP, PORT))
#Listening for any incoming connections
s.listen()

#connections dictionary to store all the connections
connections = {}

#Receiving input from users and sending it to all the other users (Texting~)
def distribute(c, a):
    #Since this runs as a custom thread for every user, it'll continously check the connection
    while True:
        #If the client is still in contact with the server
        try:
            reply = c.recv(1024)
        #If the client has lost the connection with the server
        except:
            notif = connections[c] + " has left the chat :("
            print(notif)
            connections.pop(c)
            for user in connections:
                user.send(notif.encode())
            break
        if not reply:
            notif = connections[c] + " has left the chat :("
            print(notif)
            connections.pop(c)
            for user in connections:
                user.send(notif.encode())
            break
        #If the user sent a message then distribute it to everyone else
        reply = connections[c]+" : "+reply.decode()
        for user in connections:
            user.send(reply.encode())

#When a client makes a connection to join the server
def join(c, a):
    #Asking the user for a username
    c.send("Username?".encode())
    name = c.recv(1024)

    #Checking if the username is unique
    if name.decode() in connections.values():
        c.send(">_< Username already exists".encode())
        join(c, a)
        return
    
    #Storing the connection
    connections[c] = name.decode()

    #Letting everyone else in the chat know about the new user
    for user in connections:
        new_user = name.decode() + " has joined the chat! :)"
        user.send(new_user.encode())

    #A server-side log of user's entry
    print(new_user)

    #Creating a new thread for client (Each client has a different thread so that each connection can be handled appropriately)
    cthread = threading.Thread(target=distribute, args=(c, a))
    cthread.daemon = True
    cthread.start()

#Running the server
print("Server Running...")
while True:
    c, a = s.accept()
    jthread = threading.Thread(target=join, args=(c, a))
    jthread.daemon = True
    jthread.start()
