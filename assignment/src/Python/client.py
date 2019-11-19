#coding: utf-8
import sys, os
from socket import *
import threading
import time

MIN_ARGS = 3
MAX_PORT_NO = 65535
BUFSIZ = 512

# a simple struct for holding client information
class ClientInformation():
    def __init__(self):
        self.username = None
        self.password = None
        self.peerIP = None
        self.peerPort = None
clientInfo = ClientInformation()

class Responses():

    # generic success message with 0..* strings, returns True if needed
    def response_OK(self, args):
        print(f"running response OK in client with args {args}")
        for string in args:
            print(string)
        return True
    
    # generic failure message with 0..* strings, returns False if needed
    def response_NOTOK(self, args):
        for string in args:
            print(string)
        return False

    # server rejected username, so get a new one (+ password)
    def response_BADUSER(self, args):
        for string in args:
            print(string)
        clientInfo.username = input("username: ")
        clientInfo.password = input("password: ")
        request_with([clientInfo.username, clientInfo.password])
        return False

    def reponse_BADPASS(self, args):
        print("might not need this")

    def response_LOGOUT(self, args):
        for string in args:
            print(string)
        os._exit(0)

    def run(self, response):
        keyword = response.split("\n")[0]
        args = response.split("\n")[1:]
        response_handler = getattr(self, "response_"+keyword, None)
        if response_handler is not None:
            return response_handler(args)

# create a single instance of this class for the sending/requesting thread to use
responseHandler = Responses()

def recv_responses():
    while True:
        response = serverSocket.recv(BUFSIZ).decode("utf-8")
        print("being handled by recv in response handler")
        responseHandler.run(response)

def request_whoelse(data):
    #print(f"running request whoelse with string = {request}")
    request_with(["WHOELSE"])

def request_whoelsesince(data):
    print(f"running request whoelse with string = {data}")
    if data is None:
        print("Error. No duration specified.")
        return
    request_with(["WHOELSESINCE", data])

def request_block(data):
    print(f"running request block with string = {data}")
    if data is None:
        print("Error. No user specified.")
        return
    request_with(["BLOCK", data])

def request_unblock(data):
    print(f"running request unblock with string = {data}")
    if data is None:
        print("Error. No user specified.")
        return
    request_with(["UNBLOCK", data])

def request_broadcast(data):
    print(f"running request message with string = {data}")
    if data is None:
        print("Error. No message specified.")
        return
    request_with(["BROADCAST", data])

def request_message(data):
    print(f"running request message with string = {data}")
    if data is None:
        print("Error. No message specified.")
        return
    request_with(["MESSAGE", data])

def request_logout(data):
    #print(f"running request logout with string {request}")
    request_with(["LOGOUT"])

requests = {
    "whoelse" : request_whoelse,
    "whoelsesince" : request_whoelsesince,
    "block" : request_block,
    "unblock" : request_unblock,
    "broadcast" : request_broadcast,
    "message" : request_message,
    "logout" : request_logout
}

def send_requests():

    while True:
        request = input()
        if len(request.split(" ")) > 1:
            keyword, data = request.split(" ", 1)
        else:
            keyword = request
            data = None
        print(f"keyword in client is: {keyword}, data is {data}")
        request_handler = requests.get(keyword)
        if request_handler is None:
            print("Error. Unknown request")
        else:
            request_handler(data)

def login():
    authenticated = False
    clientInfo.username = input("username: ")
    clientInfo.password = input("password: ")
    request_with([clientInfo.username, clientInfo.password, clientInfo.peerIP, clientInfo.peerPort])
    while not authenticated:
        keyword, response = unpack_response(serverSocket.recv(BUFSIZ))
        for string in response:
            print(string)
        if keyword == "BADUSER":
            clientInfo.username = input("username: ")
            clientInfo.password = input("password: ")
            request_with([clientInfo.username, clientInfo.password, clientInfo.peerIP, clientInfo.peerPort])
        elif keyword == "LOGOUT":
            # handle logout, for now just exit
            exit(1)
        elif keyword == "NOTOK":
            clientInfo.password = input("password: ")
            request_with([clientInfo.username, clientInfo.password, clientInfo.peerIP, clientInfo.peerPort])
        elif keyword == "OK":
            authenticated = True
        else:
            print("Uh-oh! Looks like something went wrong!")
        
def generate_request(lines):
    # make sure all list elements are strings
    lines[:] = [str(line) for line in lines]
    request = '\n'.join(lines)
    #print(f"request is:\n{request}")
    return request

def request_with(lines):
    lines = generate_request(lines)
    serverSocket.send(lines.encode())

def unpack_response(response):
    response = response.decode("utf-8")
    response = response.split("\n")
    keyword = response[0]
    return keyword, response[1:]

##############################
#           main()           #
##############################

# ensure request-line arguments were entered
if len(sys.argv) < MIN_ARGS:
    print(f"usage error: python3 {sys.argv[0]} <server_ip> <server_port>")
    exit(1)

# extract request line arguments
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
clientInfo.peerIP, clientInfo.peerPort = peerSocket.getsockname()

# authenticate with the server
login()

# create a receiving/response handling thread
recvThread = threading.Thread(name="recvThread", target=recv_responses)
recvThread.daemon=True
recvThread.start()

# and also create an input/request sending thread
sendThread = threading.Thread(name="sendThread", target=send_requests)
sendThread.daemon=True
sendThread.start()

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