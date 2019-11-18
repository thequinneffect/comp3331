#python3

import sys
from socket import *
import threading

import time # only needed for testing atm

MIN_ARGS = 4
MAX_PORT_NO = 65535
BUFSIZ = 512
MAX_LOGIN_ATTEMPTS = 3

threadLock = threading.Condition()

class Client():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.clientSocket = None
        self.peeringInfo = None
        self.isBlocked = False
        self.isOnline = False
        self.triesLeft = 3
        #self.loginTime = None
        #self.Timer # not sure if this goes here or is an object or not, but represents the per user time that is set after each command
        #self.offlineMessages = [] # append to this when they aren't online
        #self.blockedClients = [] # can do if username in blockedClients to check i.e. only stores username of blocked client, not struct

clients = {}

# request pattern credit: https://stackoverflow.com/questions/42227477/call-a-function-from-a-stored-string-in-python
class Requests():

    # given a username and password, either logs in if valid and return true
    # or doesn't and returns false
    def request_AUTH(self, clientSocket, args):
        print(f"running the AUTH request on server with arg={args}")
        username = args[0]
        password = args[1]
        # check if the user exists
        

    def request_LOGOUT(self, clientSocket, args):
        print(f"got a logout request on socket {clientSocket}")

    def run(self, clientSocket, req):
        keyword = req.split("\n")[0]
        req = req.split("\n")[1:]
        request = getattr(self, "request_"+keyword, None)
        if request is not None:
            return request(clientSocket, req)

requestHandler = Requests()

def authenticate(clientSocket):
    authenticated = False
    clientInfo = clientSocket.recv(BUFSIZ).decode("utf-8").split("\n")
    username = clientInfo[0]
    password = clientInfo[1]
    peerIP = clientInfo[2]
    peerPort = clientInfo[3]
    while not authenticated:
        clientInfo = clientSocket.recv(BUFSIZ).decode("utf-8").split("\n")
        username = clientInfo[0]
        password = clientInfo[1]
        if username not in client_creds:
            respond_with(clientSocket, ["BADUSER", "Please enter a valid username."])
            continue
        # user exists, so now check if already online or blocked
        client = clients[username]
        # cannot be blocked and online, so check blocked first
        if client.isBlocked:
            respond_with(clientSocket, ["BADUSER", "Account is currently blocked."])
            return False
        elif client.isOnline:
            respond_with(clientSocket, ["BADUSER", "Account is already logged in."])
            return False
        # eligible for login, so check the password is correct
        elif client.password != password:
            client.triesLeft -= 1
            if client.triesLeft <= 0:
                client.isBlocked = True
                respond_with(clientSocket, ["LOGOUT", "Invalid password. Your account has been blocked. Please try again later"])
            else:
                respond_with(clientSocket, ["NOTOK", "Invalid password. Please try again"])
            return False
        # valid, so login and setup client information
        else:
            respond_with(clientSocket, ["OK", "Welcome to the server."])
            client.triesLeft = 3
            client.clientSocket = clientSocket
            client.isOnline = True
            client.peerIP = peerIP
            client.peerPort = peerPort
            return True

def new_client_handler(ip, port, clientSocket):
    print(f"new client handler made for client: {ip}:{port} with socket {clientSocket}")

    authenticate(clientSocket)

    print("going into servicing loop...")
    while True:
        print("about to recv")
        request = clientSocket.recv(BUFSIZ).decode("utf-8")
        # if the client socket has closed, then close this thread
        if request is None:
            return
        # client is active! reset timer
        clients[clientSocket]
        print("about to run")
        requestHandler.run(clientSocket, request)
        
def generate_response(lines):
    lines[:] = [str(line) for line in lines]
    response = '\n'.join(lines)
    print(f"response is:\n{response}")
    return response

def respond_with(clientSocket, lines):
    response = generate_response(lines)
    clientSocket.send(response.encode())

def unpack_request(request):
    request = request.decode("utf-8")
    request = request.split("\n")
    keyword = request[0]
    return keyword, request[1:]

##############################
#           main()           #
##############################

# ensure enough command line arguments were passed 
if len(sys.argv) < MIN_ARGS:
    print(f"usage error: python3 {sys.argv[0]} <server_port> <block_duration> <timeout>")
    exit(1)

# extract command line arguments
serverPort = int(sys.argv[1])
if serverPort not in range(1, MAX_PORT_NO+1):
    print(f"usage error: port number {serverPort} is invalid")
    exit(1)
blockDuration = int(sys.argv[2])
timeoutTimer = int(sys.argv[3])

client_creds = {}
credentials = open("./credentials.txt","r")
for cred in credentials:
    cred = cred.rstrip('\n')
    username, password = cred.split(" ")
    client_creds[username] = password
    #clients[username] = Client(username, password)

#for username in client_creds:
#    print(f"username: {username}, password: {client_creds[username]}")

# setup the server welcoming socket with ipv4 and tcp
welcomeSocket = socket(AF_INET, SOCK_STREAM)
# make able to reuse port even if it is in the time wait state
welcomeSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# this server is listening on this machine at port 12000
welcomeSocket.bind(('localhost', serverPort))

# listen and only refuse max once
welcomeSocket.listen(1)
print("TCP Server now listening!")

while 1:

    # create a socket specifically for the client that has just requested a connection
    clientSocket, addr = welcomeSocket.accept()
    clientArgs = [addr[0], addr[1], clientSocket]
    print(addr)
    print(clientSocket)

    clientThread = threading.Thread(name="clientThread", target=new_client_handler, args=clientArgs)
    clientThread.daemon=True
    clientThread.start()