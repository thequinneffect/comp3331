#python3

import sys
from socket import *
import threading

MIN_ARGS = 4
MAX_PORT_NO = 65535
BUFSIZ = 512
MAX_LOGIN_ATTEMPTS = 3



# command pattern credit: https://stackoverflow.com/questions/42227477/call-a-function-from-a-stored-string-in-python
class Commands():

    # given a username and password, either logs in if valid and return true
    # or doesn't and returns false
    def command_AUTH(self, args):
        print(f"running the AUTH command on server with arg={args}")
        username = args[0]
        password = args[1]
        if username not in client_creds:
            return False
        if client_creds[username] != password:
            return False
        return True

    def run(self, req):
        keyword = req.split("\n")[0]
        req = req.split("\n")[1:]
        command = getattr(self, "command_"+keyword, None)
        if command is not None:
            return command(req)

def new_client_handler(ip, port, sock):
    print(f"new client handler made for client: {ip}:{port}")

    if not authenticate(sock):
        exit(1)
    print("client was authenticated, going into service loop")
    while True:
        req = sock.recv(BUFSIZ).decode("utf-8")
        print(req)

def authenticate(sock):

    commands = Commands()
    authenticated = False
    tryCount = 1
    while not authenticated:
        # expecting client to send credentials
        req = sock.recv(BUFSIZ).decode("utf-8")
        authenticated = commands.run(req)
        if not authenticated:
            response = generate_response(["NOTOK", "Try again"])
            tryCount += 1
        if tryCount > MAX_LOGIN_ATTEMPTS:
            response = generate_response(["LOGOUT"])
            sock.send(response.encode())
            break
        if authenticated:
            response = generate_response(["OK", "Welcome to the server!"])
        sock.send(response.encode())
        
def generate_response(lines):
    response = '\n'.join(lines)
    print(f"response is:\n{response}")
    return response


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
    connectionSocket, addr = serverSocket.accept()
    clientArgs = [addr[0], addr[1], connectionSocket]

    clientThread = threading.Thread(name="clientThread", target=new_client_handler, args=clientArgs)
    clientThread.daemon=True
    clientThread.start()






























    '''
    # wait whilst trying to receive data from the client on its dedicated connection socket
    client_sentence = connectionSocket.recv(1024)

    client_sentence = client_sentence.decode("utf-8")

    new_user, new_pass = client_sentence.split(" ")
    print(f"new user is: {new_user}, new pass is: {new_pass}")

    if new_user in clients and clients[new_user] == new_pass:
        reply = "OK"
    else:
        reply = "!OK"

    #reply = str.encode(client_sentence.upper())
    print(f"replying with: {reply}")
    reply = str.encode(reply, "utf-8")
    connectionSocket.send(reply)

    connectionSocket.close()
    '''