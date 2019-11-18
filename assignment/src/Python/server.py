#python3

import sys
from socket import *
import threading
import datetime

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
        self.peerIP = None
        self.peerPort = None
        self.isBlocked = False
        self.blockTime = None
        self.isOnline = False
        self.triesLeft = 3
        self.loginTime = None
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
        peerIP = args[2]
        peerPort = args[3]
        # check if the user exists
        if username not in client_creds:
            respond_with(clientSocket, ["BADUSER", "Please enter a valid username."])
            return False
        # user exists, so now check if already online or blocked
        client = clients[username]
        # unblock if blocktime has elapsed
        currentTime = time.time()
        if client.isBlocked and currentTime - client.blockTime >= blockDuration:
            client.isBlocked = False
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
                client.blockTime = time.time()
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
            # also set up the peering info before the client enters servicing loop and is deemed online
            client.peerIP = peerIP
            client.peerPort = peerPort
            client.loginTime = time.time()
            client.timer = threading.Timer(timeoutTime, handle_timeout, args=[client.clientSocket])
            client.timer.start()
            return True

    def request_LOGOUT(self, clientSocket, args):
        print(f"got a logout request on socket {clientSocket}")
        # TODO: do any cleanup needed with client structure
        respond_with(clientSocket, ["LOGOUT", "You have been logged out of the server."])

    def run(self, clientSocket, req):
        keyword = req.split("\n")[0]
        req = req.split("\n")[1:]
        request = getattr(self, "request_"+keyword, None)
        if request is not None:
            return request(clientSocket, req)
        else:
            print("Error: ill-formatted request from server")
            

requestHandler = Requests()

def handle_timeout(clientSocket):
    respond_with(clientSocket, ["LOGOUT", "You have been logged out due to inactivity."])

def new_client_handler(ip, port, clientSocket):
    print(f"new client handler made for client: {ip}:{port} with socket {clientSocket}")

    print("going into servicing loop...")
    while True:
        print("about to recv")
        request = clientSocket.recv(BUFSIZ).decode("utf-8")
        print(request)
        # if the client socket has closed, then close this thread
        if len(request) == 0:
            sys.exit() # TODO: replace with function that cleans up the exited clients struct
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
timeoutTime = int(sys.argv[3])

client_creds = {}
credentials = open("./credentials.txt","r")
for cred in credentials:
    cred = cred.rstrip('\n')
    username, password = cred.split(" ")
    #print(f"{username},{len(username)}")
    #print(f"{password},{len(password)}")
    client_creds[username] = password
    clients[username] = Client(username, password)

for username in client_creds:
    print(f"username: {username}, password: {client_creds[username]}")

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

    clientThread = threading.Thread(name="clientThread", target=new_client_handler, args=clientArgs)
    clientThread.daemon=True
    clientThread.start()