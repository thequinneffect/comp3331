#python3

import sys
from socket import *
import threading

import time # only needed for testing atm

MIN_ARGS = 4
MAX_PORT_NO = 65535
BUFSIZ = 512
MAX_LOGIN_ATTEMPTS = 3

class Client():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.clientSocket = None
        self.peeringInfo = None
        self.isBlocked = False
        self.isOnline = False
        #self.loginTime = None
        #self.Timer # not sure if this goes here or is an object or not, but represents the per user time that is set after each command
        #self.offlineMessages = [] # append to this when they aren't online
        #self.blockedClients = [] # can do if username in blockedClients to check i.e. only stores username of blocked client, not struct

clients = {}

# request pattern credit: https://stackoverflow.com/questions/42227477/call-a-function-from-a-stored-string-in-python
class Requests():

    # given a username and password, either logs in if valid and return true
    # or doesn't and returns false
    def request_AUTH(self, args):
        print(f"running the AUTH request on server with arg={args}")
        username = args[0]
        password = args[1]
        if username not in client_creds:
            respond_with(["NOUSER"])
        if client_creds[username] != password:
            # decrement tries left for this client
            # if client.tries left is 0
                # respond with logout and block
            respond_with(["NOTOK", "Try again"])
        # valid, so login and setup info
        return True

    def run(self, req):
        keyword = req.split("\n")[0]
        req = req.split("\n")[1:]
        request = getattr(self, "request_"+keyword, None)
        if request is not None:
            return request(req)

requestHandler = Requests()

def new_client_handler(ip, port, clientSocket):
    print(f"new client handler made for client: {ip}:{port}")

    isAuthenticated = authenticate(clientSocket)
    if not isAuthenticated:
        print("TODO: implement clean up here")
        time.sleep(0.1)

    print("going into servicing loop...")
    while True:
        time.sleep(0.1)
        print("service service ...")

def authenticate(clientSocket):
    triesLeft = 3
    while True:
        print(f"attempting aithentication with {triesLeft} tries left")
        # protocol expects client to send credentials now
        req = clientSocket.recv(BUFSIZ).decode("utf-8")
        req = req.split("\n")
        username = req[0]
        password = req[1]
        peerIP = req[2]
        peerPort = req[3]
        print(f"details for authenticating are: {username} {password} {peerIP} {peerPort}")

        # check if the user exists
        if username not in client_creds:
            respond_with(["BADUSER", "Please enter a valid username."])
            # cannot decrement tries or block non-existant user, so demand valid username
            # and reset the number of tries
            triesLeft = 3
            continue
        # user exists, so now check if already online or blocked
        client = clients[username]
        # cannot be blocked and online, so check blocked first
        if client.isBlocked:
            respond_with(["BADUSER", "Account is currently blocked."])
            return False
        elif client.isOnline:
            respond_with(["BADUSER", "Account is already logged in."])
            return False
        # eligible for login, so check the password is correct
        elif client.password != password:
            triesLeft -= 1
            if triesLeft <= 0:
                client.isBlocked = True
                respond_with(["LOGOUT", "Invalid Password. Your account has been blocked. Please try again later"])
                return False
            else:
                respond_with(["NOTOK", "Invalid Password. Please try again"])
        # valid, so login configure current host information
        else:
            client.clientSocket = clientSocket
            client.peerIP = peerIP
            client.peerPort = peerPort
            respond_with(["OK", "Welcome to the server."])
            return True
        
def generate_response(lines):
    lines[:] = [str(line) for line in lines]
    response = '\n'.join(lines)
    print(f"response is:\n{response}")
    return response

def respond_with(lines):
    response = generate_response(lines)
    clientSocket.send(response.encode())

##############################
#           main()           #
##############################

# ensure enough command line arguments were passed 
if len(sys.argv) < MIN_ARGS:
    print(f"usage error: python3 {sys.argv[0]} <server_port> <block_duration> <timeout>")
    exit(1)

# extracr command line arguments
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