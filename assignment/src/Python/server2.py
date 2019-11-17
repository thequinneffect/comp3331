#python3

import sys
from socket import *
import threading

import time # only needed for testing atm

MIN_ARGS = 4
MAX_PORT_NO = 65535
BUFSIZ = 512
MAX_LOGIN_ATTEMPTS = 3

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

def new_client_handler(ip, port, sock):
    print(f"new client handler made for client: {ip}:{port}")
    while True:
        req = sock.recv(BUFSIZ).decode("utf-8")
        requestHandler.run(req)

def authenticate(sock):

    authenticated = False
    tryCount = 1
    while not authenticated:
        print("in auth loop")
        # expecting client to send credentials
        req = sock.recv(BUFSIZ).decode("utf-8")
        authenticated = requestHandler.run(req)
        if not authenticated:
            response = generate_response(["NOTOK", "Try again"])
            tryCount += 1
        if tryCount > MAX_LOGIN_ATTEMPTS:
            response = generate_response(["LOGOUT"])
            sock.send(response.encode())
            break
        if authenticated:
            response = generate_response(["OK", "Welcome to the server!"])
        print(f"before send: auth is {authenticated}")
        sock.send(response.encode())
        print(f"after send: auth is {authenticated}")
    return authenticated
        
def generate_response(lines):
    lines[:] = [str(line) for line in lines]
    response = '\n'.join(lines)
    print(f"response is:\n{response}")
    return response

def respond_with(lines):
    response = generate_response(lines)
    serverSocket.send(response.encode())

if len(sys.argv) < MIN_ARGS:
    print(f"usage error: python3 {sys.argv[0]} <server_port> <block_duration> <timeout>")
    exit(1)

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

for username in client_creds:
    print(f"username: {username}, password: {client_creds[username]}")

# use ipv4 and tcp
serverSocket = socket(AF_INET, SOCK_STREAM)
# make able to reuse port even if it is in the time wait state
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# this server is listening on this machine at port 12000
serverSocket.bind(('localhost', serverPort))

# listen and only refuse max once
serverSocket.listen(1)
print("TCP Server now listening!")

while 1:

    # create a socket specifically for the client that has just requested a connection
    clientSocket, addr = serverSocket.accept()
    clientArgs = [addr[0], addr[1], clientSocket]

    clientThread = threading.Thread(name="clientThread", target=new_client_handler, args=clientArgs)
    clientThread.daemon=True
    clientThread.start()