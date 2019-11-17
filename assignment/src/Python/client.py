#coding: utf-8
import sys
from socket import *

MIN_ARGS = 3
MAX_PORT_NO = 65535
BUFSIZ = 512

class Responses():

    # given a username and password, either logs in if valid and return true
    # or doesn't and returns false
    def response_OK(self, args):
        print("running response handler for OK response")
        print(args[0])
        return True
    
    def response_NOTOK(self, args):
        print("running response handler for NOTOKAY response")
        print(args[0])
        return False

    def response_LOGOUT(self, args):
        exit(1)

    def run(self, response):
        keyword = response.split("\n")[0]
        args = response.split("\n")[1:]
        response_handler = getattr(self, "response_"+keyword, None)
        if response_handler is not None:
            return response_handler(args)

def client_loop():
    login()
    while True:
        new_command = input("> ")
        print(new_command)
        clientSocket.send(new_command.encode())

def login():
    authenticated = False
    while not authenticated:
        username = input("username: ")
        password = input("password: ")
        command = generate_command(["AUTH", username, password])
        clientSocket.send(command.encode())
        reply = clientSocket.recv(BUFSIZ).decode("utf-8")
        response_handler = Responses()
        authenticated = response_handler.run(reply)
        
def generate_command(lines):
    command = '\n'.join(lines)
    print(f"command is:\n{command}")
    return command

if len(sys.argv) < MIN_ARGS:
    print(f"usage error: python3 {sys.argv[0]} <server_ip> <server_port>")
    exit(1)

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
if serverPort not in range(1, MAX_PORT_NO+1):
    print(f"usage error: invalid port number, please use a port number in range [0, {MAX_PORT_NO}]")
    exit(1)

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverIP, serverPort))

client_loop()

clientSocket.close()
#and close the socket


# TODO:
"""
    - 1 thread for sending to server (typing input and sending requests), 1 thread for receiving from server (servicing responses),
    and another thread for p2p (or another 2 threads for peer to peer, peer sending and peer receiving?) 
        - you have just 1 extra socket (actually a new port but whatever) for the peer to peer, but one (or maybe need two) new threads
        per peer that joins
        - If using Python, check socket.bind((' ', 0)). needed for getting unique client port num for each new client
"""