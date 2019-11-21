# PYTHON 3 - z5117408
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
        self.peerSocket = None
clientInfo = ClientInformation()
peers = {}

class Responses():

    # generic success message with 0..* strings, returns True if needed
    def response_OK(self, args):
        for string in args:
            print(string)
        return True
    
    # generic failure message with 0..* strings, returns False if needed
    def response_NOTOK(self, args):
        for string in args:
            print(string)
        return False

    def response_STARTPRIVATE(self, args):
        peerIP = args[0]
        peerPort = int(args[1])
        peerUsername = args[2]
        newPeerSocket = socket(AF_INET, SOCK_STREAM)
        newPeerSocket.connect((peerIP,peerPort))
        newPeerSocket.send(clientInfo.username.encode())
        if peerUsername not in peers:
            peers[peerUsername] = ClientInformation()
        otherPeer = peers[peerUsername]
        otherPeer.username = peerUsername
        otherPeer.peerSocket = newPeerSocket
        print(f"A private connection with {peerUsername} has been started.")
        start_peering_thread(newPeerSocket)

    def response_STOPPRIVATE(self, args):
        peerUsername = args[0]
        remove_peer(peerUsername)

    def response_LOGOUT(self, args):
        for string in args:
            print(string)
        peerUsernames = [username for username in peers]
        for peerUsername in peerUsernames: request_stopprivate(peerUsername)
        os._exit(0)

    def run(self, response):
        keyword = response.split("\n")[0]
        args = response.split("\n")[1:]
        response_handler = getattr(self, "response_"+keyword, None)
        if response_handler is not None:
            return response_handler(args)

# create a single instance of this class for the sending/requesting thread to use
responseHandler = Responses()

# the receiver of responses for the server
def recv_responses():
    while True:
        response = serverSocket.recv(BUFSIZ).decode("utf-8")
        responseHandler.run(response) # find and run correct response handling function

# ALL OF THE REQUESTS THAT THE CLIENT HAS AVAILABLE TO THEM
# Bascially just do appropriate checks and then request_with(requestkeyword, args...)
def request_whoelse(data):
    request_with(["WHOELSE"])

def request_whoelsesince(data):
    if data is None:
        print("Error. No duration specified.")
        return
    request_with(["WHOELSESINCE", data])

def request_block(data):
    if data is None:
        print("Error. No user specified.")
        return
    request_with(["BLOCK", data])

def request_unblock(data):
    if data is None:
        print("Error. No user specified.")
        return
    request_with(["UNBLOCK", data])

def request_broadcast(data):
    if data is None:
        print("Error. No message specified.")
        return
    request_with(["BROADCAST", data])

def request_message(data):
    if data is None:
        print("Error. No message specified.")
        return
    username, message = data.split(" ", 1)
    request_with(["MESSAGE", username, message])

def request_startprivate(peerUsername):
    if peerUsername is None:
        print("Error. No user specified.")
        return
    elif peerUsername in peers:
        print(f"Error. A private connection with {peerUsername} already exists.")
    else:
        request_with(["STARTPRIVATE", peerUsername])

def request_private(data):
    if data is None:
        print("Error. No user or message specified.")
        return
    username, message = data.split(" ", 1)
    message = clientInfo.username + "(private): " + message
    if username == clientInfo.username:
        print(f"Error. You cannot private message yourself.")
        return
    elif username not in peers:
        print(f"Error. No private connection with {username} exists.")
        return
    try:
        peerMessage = generate_request(["OK", message])
        peers[username].peerSocket.send(peerMessage.encode())
    except error:
        print(f"Private connection with {username} has closed.")

def request_stopprivate(username):
    if username is None:
        print("Error. No user or message specified.")
        return
    if username == clientInfo.username:
        print(f"Error. No private connection exists with yourself.")
        return
    elif username not in peers:
        print(f"Error. No private connection with {username} exists.")
        return
    message = generate_request(["STOPPRIVATE", clientInfo.username])
    peers[username].peerSocket.send(message.encode())
    remove_peer(username)

def request_logout(data):
    request_with(["LOGOUT"])

def remove_peer(peerUsername):
    peers[peerUsername].peerSocket.close()
    del peers[peerUsername]
    print(f"The private connection with {peerUsername} has ended.")

# dictionary that acts as a dispatch table for requests (based on keyword)
requests = {
    "whoelse" : request_whoelse,
    "whoelsesince" : request_whoelsesince,
    "block" : request_block,
    "unblock" : request_unblock,
    "broadcast" : request_broadcast,
    "message" : request_message,
    "startprivate" : request_startprivate,
    "private" : request_private,
    "stopprivate" : request_stopprivate,
    "logout" : request_logout
}

# infinite loop for sending requests to the server or peers
def send_requests():

    while True:
        request = input()
        # if it is a request that takes arguments then get them
        if len(request.split(" ")) > 1:
            keyword, data = request.split(" ", 1)
        else:
            keyword = request
            data = None
        # get the appropriate request handler via the keyword
        request_handler = requests.get(keyword)
        if request_handler is None:
            print("Error. Unknown request")
        else:
            request_handler(data) # call it with the arguments

# authenticate with the server
def login():
    authenticated = False
    clientInfo.username = input("username: ")
    clientInfo.password = input("password: ")
    # send authentication information to the server which is expecting it
    request_with([clientInfo.username, clientInfo.password, clientInfo.peerIP, clientInfo.peerPort])
    while not authenticated:
        # wait for server response
        keyword, response = unpack_response(serverSocket.recv(BUFSIZ))
        for string in response: 
            print(string) # print the information the server provided regardless of status
        # now act based on keyword - self explanatory as keywords are human readable!
        if keyword == "BADUSER":
            clientInfo.username = input("username: ")
            clientInfo.password = input("password: ")
            request_with([clientInfo.username, clientInfo.password, clientInfo.peerIP, clientInfo.peerPort])
        elif keyword == "LOGOUT":
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
    request = '\n'.join(lines) # join them with newline separators
    return request

# generate a newline separated request from lines, then send it to the server
def request_with(lines):
    lines = generate_request(lines)
    serverSocket.send(lines.encode())

# unpack the newline separated response from server/peer
def unpack_response(response):
    response = response.decode("utf-8")
    response = response.split("\n")
    keyword = response[0]
    return keyword, response[1:]

def start_peering_thread(peerSocket):
    peerThread = threading.Thread(name="peerThread", target=new_peer_handler, args=[peerSocket])
    peerThread.daemon=True
    peerThread.start()

# receiver for peers
def new_peer_handler(peerSocket):
    while True:
        try:
            response = peerSocket.recv(BUFSIZ).decode("utf-8")
            responseHandler.run(response)
        except error:
            # socket error so exit, not required to handle properly by spec
            sys.exit(0)

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
peerWelcomeSocket = socket(AF_INET, SOCK_STREAM)

# bind to port #0 to let OS pick a currently unused port (ensure clients have different port)
peerWelcomeSocket.bind((gethostbyname(gethostname()), 0))
clientInfo.peerIP, clientInfo.peerPort = peerWelcomeSocket.getsockname()
peerWelcomeSocket.listen(1)

# force authentication with the server
login()

# create a receiving/response handling thread
recvThread = threading.Thread(name="recvThread", target=recv_responses)
recvThread.daemon=True
recvThread.start()

# and also create an input/request sending thread
sendThread = threading.Thread(name="sendThread", target=send_requests)
sendThread.daemon=True
sendThread.start()

# and now listen on the peering socket for any peer connections
while True:
    peerSocket, addr = peerWelcomeSocket.accept()

    # protocol is that the active peer (one who started peering)
    # will send its username to the passive peer (this one)
    otherClientUsername = peerSocket.recv(BUFSIZ).decode("utf-8")
    if otherClientUsername not in peers:
        peers[otherClientUsername] = ClientInformation()
    # setup peer information
    otherClient = peers[otherClientUsername]
    otherClient.username = otherClientUsername
    otherClient.peerSocket = peerSocket
    print(f"{otherClientUsername} has started a private connection with you.")
    # start a new thread for accepting requests for this peer
    start_peering_thread(peerSocket)