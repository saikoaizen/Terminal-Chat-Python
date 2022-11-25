import socket
import threading

#Creating a socket to make a connection to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Server details
IP = ""
PORT = 0000

#Making a connection to the server
s.connect((IP,PORT))

#Sending input from the client
def send():
    while True:
        try:
            s.send(input("").encode())
        except:
            break
    s.close()

#Starting a thread so that reception and transmission can be done simultaneously
st =  threading.Thread(target=send)
st.daemon = True
st.start()

#Running the client
while True:
	rep = s.recv(1024)
	print(rep.decode())