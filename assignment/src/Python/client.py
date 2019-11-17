#coding: utf-8
import sys
from socket import *
import threading
import time

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

    def reponse_NOUSER(self, args):
        print("Invalid username. Please enter a valid username.")
        login()

    def response_LOGOUT(self, args):
        exit(1)

    def run(self, response):
        keyword = response.split("\n")[0]
        args = response.split("\n")[1:]
        response_handler = getattr(self, "response_"+keyword, None)
        if response_handler is not None:
            return response_handler(args)

# create a single instance of this class for the sending/requesting thread to use
responseHandler = Responses()

def response_receiver():
    response = serverSocket.recv(BUFSIZ).decode("utf-8")
    print("being handled by recv in response handler")
    responseHandler.run(response)


def request_message(words):
    print(f"running request msg with words = {words}")

requests = {
    "msg" : request_message
}

def request_sender():
    while True:
        request = input()
        words = request.split(" ")
        requestFunc = requests.get(words[0])
        if requestFunc is None:
            print("Error: unknown command")
        else:
            requestFunc(words[1:])


def login():
    authenticated = False
    username = input("username: ")
    while not authenticated:
        password = input("password: ")
        command = generate_command(["AUTH", username, password, peerIP, peerPort])
        serverSocket.send(command.encode())
        response = serverSocket.recv(BUFSIZ).decode("utf-8")
        authenticated = responseHandler.run(response)

# configure details like peering information
# allows server to do setup before considering client "online"
def init():
    print("peering information being sent!")
    request = generate_command(["INIT", peerIP, peerPort])
    serverSocket.send(request.encode())
        
def generate_command(lines):
    # make sure all list elements are strings
    lines[:] = [str(line) for line in lines]
    command = '\n'.join(lines)
    #print(f"command is:\n{command}")
    return command

# START #

# ensure command-line arguments were entered
if len(sys.argv) < MIN_ARGS:
    print(f"usage error: python3 {sys.argv[0]} <server_ip> <server_port>")
    exit(1)

# extract command line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
if serverPort not in range(1, MAX_PORT_NO+1):
    print(f"usage error: invalid port number, please use a port number in range [0, {MAX_PORT_NO}]")
    exit(1)

# create the local socket for communicating with the remote server
serverSocket = socket(AF_INET, SOCK_STREAM)
# and connect to it
serverSocket.connect((serverIP, serverPort))

# now create the local socket this client will be using for P2P messaging
peerSocket = socket(AF_INET, SOCK_STREAM)
# bind to port #0 to let OS pick a currently unused port (ensure clients have different port)

peerSocket.bind((gethostbyname(gethostname()), 0))
peerIP, peerPort = peerSocket.getsockname()

# authenticate with the server
login()
# configure details before entering service loop e.g. P2P info
init()

# create a receiving/response handling thread
recvThread = threading.Thread(name="clientThread", target=response_receiver)
recvThread.daemon=True
recvThread.start()

# and also create an input/request sending thread
sendThread = threading.Thread(name="sendThread", target=request_sender)
sendThread.daemon=True
sendThread.start()

#serverSocket.close()
#and close the socket
while True:
    time.sleep(0.1)


# TODO:
"""
    - 1 thread for sending to server (typing input and sending requests), 1 thread for receiving from server (servicing responses),
    and another thread for p2p (or another 2 threads for peer to peer, peer sending and peer receiving?) 
        - you have just 1 extra socket (actually a new port but whatever) for the peer to peer, but one (or maybe need two) new threads
        per peer that joins
        - If using Python, check socket.bind((' ', 0)). needed for getting unique client port num for each new client
"""