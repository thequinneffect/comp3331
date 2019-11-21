# PYTHON 3 - z5117408
import sys
from socket import *
import threading
import datetime
import time

MIN_ARGS = 4
MAX_PORT_NO = 65535
BUFSIZ = 512
MAX_LOGIN_ATTEMPTS = 3

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
        self.logoutTime = None
        self.timer = None
        self.offlineMessages = [] # stores the messages as strings
        self.blockedClients = [] # stores username strings, not client structs

    def setLogoutInfo(self):
        self.cilentSocket = None
        self.isOnline = False
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
        self.logoutTime = time.time()

    def showPresence(self, logDirection):
        for username in clients:
            if username == self.username:
                continue
            otherClient = clients[username]
            if not otherClient.isOnline:
                continue
            if otherClient.username not in self.blockedClients:
                respond_with(otherClient.clientSocket, ["OK", f"{self.username} has logged {logDirection}."])

    def showOfflineMessages(self):
        if len(self.offlineMessages) > 0:
            response = '\n'.join(self.offlineMessages)
            respond_with(self.clientSocket, ["OK", response])
            self.offlineMessages.clear()

# one entry of the above structure per client in credentials list
clients = {}

# command pattern credit: https://stackoverflow.com/questions/42227477/call-a-function-from-a-stored-string-in-python
class Requests():

    def request_WHOELSE(self, client, args):
        otherClients = ["OK"] # responding with OK
        for username in clients:
            otherClient = clients[username]
            if otherClient is not client and otherClient.isOnline:
                otherClients.append(otherClient.username)
        if len(otherClients) == 1:
            otherClients.append("Nobody else is online.")
        respond_with(client.clientSocket, otherClients) # prepended with an "OK" response keyword

    def request_WHOELSESINCE(self, client, args):
        sinceTime = int(args[0])
        timeAgo = time.time() - sinceTime
        otherClients = ["OK"] # responding with OK
        for username in clients:
            if username == client.username:
                continue
            otherClient = clients[username]
            if otherClient.isOnline or (otherClient.logoutTime is not None and otherClient.logoutTime > timeAgo):
                otherClients.append(otherClient.username)
        if len(otherClients) == 1:
            otherClients.append(f"Nobody else has been online for {sinceTime} seconds.")
        respond_with(client.clientSocket, otherClients)

    def request_BLOCK(self, client, args):
        username = args[0]
        if username not in client_creds:
            respond_with(client.clientSocket, ["NOTOK", f"You cannot block {username} as they do not exist."])
        elif username == client.username:
            respond_with(client.clientSocket, ["NOTOK", "You cannot block yourself."])
        elif username in client.blockedClients:
            respond_with(client.clientSocket, ["NOTOK", f"You have already blocked {username}."])
        else:
            client.blockedClients.append(username)
            respond_with(client.clientSocket, ["OK", f"You have successfully blocked {username}."])

    def request_UNBLOCK(self, client, args):
        username = args[0]
        if username not in client_creds:
            respond_with(client.clientSocket, ["NOTOK", f"You cannot unblock {username} as they do not exist."])
        elif username == client.username:
            respond_with(client.clientSocket, ["NOTOK", "You cannot unblock yourself."])
        elif username not in client.blockedClients:
            respond_with(client.clientSocket, ["NOTOK", f"You cannot unblock {username} as you have not blocked them."])
        else:
            client.blockedClients.remove(username)
            respond_with(client.clientSocket, ["OK", f"You have successfully unblocked {username}."])

    def request_BROADCAST(self, client, args):
        message = client.username + "(broadcast): " + args[0]
        someUndelivered = False
        for username in clients:
            otherClient = clients[username]
            if otherClient.username == client.username or not otherClient.isOnline:
                continue
            elif client.username in otherClient.blockedClients:
                someUndelivered = True
            else:
                respond_with(otherClient.clientSocket, ["OK", message])
        if someUndelivered:
            respond_with(client.clientSocket, ["NOTOK", "Your message could not be delivered to some users."])

    def request_MESSAGE(self, client, args):
        username = args[0]
        message = client.username + ": " + args[1]
        if username not in client_creds:
            respond_with(client.clientSocket, ["NOTOK", f"You cannot message {username} as they do not exist."])
            return
        otherClient = clients[username]
        if otherClient.username == client.username:
            respond_with(client.clientSocket, ["NOTOK", "You cannot message yourself."])
        elif client.username in otherClient.blockedClients:
            respond_with(client.clientSocket, ["NOTOK", f"You have been blocked by {otherClient.username}."])
        elif not otherClient.isOnline:
            otherClient.offlineMessages.append(message)
        else:
            respond_with(otherClient.clientSocket, ["OK", message])

    def request_STARTPRIVATE(self, client, args):
        username = args[0]
        if username not in client_creds:
            respond_with(client.clientSocket, ["NOTOK", f"You cannot start a private connection with {username} as they do not exist."])
            return
        otherClient = clients[username]
        if otherClient.username == client.username:
            respond_with(client.clientSocket, ["NOTOK", "You cannot start a private connection with yourself."])
        elif not otherClient.isOnline:
            respond_with(client.clientSocket, ["NOTOK", f"You cannot start a private connection with {username} as they are offline."])
        elif client.username in otherClient.blockedClients:
            respond_with(client.clientSocket, ["NOTOK", f"You cannot start a private connection with {username} as they have blocked you."])
        else:
            respond_with(client.clientSocket, ["STARTPRIVATE", otherClient.peerIP, otherClient.peerPort, otherClient.username])

    def request_LOGOUT(self, client, args):
        logout(client, "You have been logged out of the server.")

    def run(self, client, req):
        keyword = req.split("\n")[0]
        req = req.split("\n")[1:]
        request = getattr(self, "request_"+keyword, None)
        if request is not None:
            return request(client, req)
        else:
            print("Error: ill-formatted request from server")
            

requestHandler = Requests()

def start_timer(client):
    client.timer = threading.Timer(timeoutTime, logout, args=[client, "You have been logged out due to inactivity."])
    client.timer.start()

def authenticate(clientSocket):
    authenticated = False
    while not authenticated:
        # receive and unpack expected client authentication information
        request = clientSocket.recv(BUFSIZ).decode("utf-8").split("\n")
        username = request[0]
        password = request[1]
        peerIP = request[2]
        peerPort = request[3]
        # check if the user exists
        if username not in client_creds:
            respond_with(clientSocket, ["BADUSER", "Please enter a valid username."])
            continue
        # user exists, so now check if already online or blocked
        client = clients[username]
        # unblock if blocktime has elapsed
        currentTime = time.time()
        if client.isBlocked and currentTime - client.blockTime >= blockDuration:
            client.isBlocked = False
        # cannot be blocked and online, so check blocked first
        if client.isBlocked:
            respond_with(clientSocket, ["BADUSER", "Account is currently blocked."])
        elif client.isOnline:
            respond_with(clientSocket, ["BADUSER", "Account is already logged in."])
        # eligible for login, so check the password is correct
        elif client.password != password:
            client.triesLeft -= 1
            if client.triesLeft <= 0:
                client.isBlocked = True
                client.triesLeft = 3
                client.blockTime = time.time()
                client.clientSocket = clientSocket # not online, so client has no clientSocket, so set to this one
                logout(client, "Invalid password. Your account has been blocked. Please try again later.")
                return None
            else:
                respond_with(clientSocket, ["NOTOK", "Invalid password. Please try again."])
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
            start_timer(client)
            client.showPresence("in")
            return client

# function called by many points when logout is needed
def logout(client, string):
    if client.isOnline:
        client.showPresence("out") # handle presence showing
    client.setLogoutInfo() # update client info to reflect logout
    respond_with(client.clientSocket, ["LOGOUT", string]) # send the logout response to client to end them
    sys.exit(0) # stop this thread as the client it services is now gone offline

def new_client_handler(ip, port, clientSocket):

    # authenticate and return client info
    client = authenticate(clientSocket)
    if client is None: # auth failed, so close this thread
        sys.exit(0)

    # retrieve any offline messages before going in to service loop
    client.showOfflineMessages()

    while True:
        try:
            request = clientSocket.recv(BUFSIZ).decode("utf-8")
            # if the client socket has closed, then close this thread
            if len(request) == 0:
                sys.exit(0)
            # got a request from the client, so restart the timeout timer
            client.timer.cancel()
            start_timer(client)
            requestHandler.run(client, request)
        except error:              
            sys.exit(0)
        
def generate_response(lines):
    lines[:] = [str(line) for line in lines]
    response = '\n'.join(lines)
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

# read in the user-password pairs from the credentials file
# store pairs in credentials dictionary and also create
# one Client() structure per client
client_creds = {}
credentials = open("./credentials.txt","r")
for cred in credentials:
    cred = cred.rstrip('\n')
    username, password = cred.split(" ")
    # map username -> password
    client_creds[username] = password
    # map username -> client information
    clients[username] = Client(username, password)

# setup the server welcoming socket with ipv4 and tcp
welcomeSocket = socket(AF_INET, SOCK_STREAM)
# make able to reuse port even if it is in the time wait state
welcomeSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# bind this socket to port <serverPort>
# always host the server locally, hence localhost
welcomeSocket.bind(('localhost', serverPort))

# listen for connections, with max client queue of size 1
welcomeSocket.listen(1)

# this is the only server message printed! just to know that it is running
print("Chat Server now online!")

while True:

    # create a socket specifically for the client that has just requested a connection
    clientSocket, addr = welcomeSocket.accept()
    # pack the args in an iterable type (list), so that the thread can accept them
    clientArgs = [addr[0], addr[1], clientSocket]

    # create a new thread specifically for this client
    clientThread = threading.Thread(name="clientThread", target=new_client_handler, args=clientArgs)
    clientThread.daemon=True
    clientThread.start()