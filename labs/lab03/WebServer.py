#python3

from socket import *

serverPort = 12000 

# use ipv4 and tcp
serverSocket = socket(AF_INET, SOCK_STREAM)

# this server is listening on this machine at port 12000
serverSocket.bind(('localhost', serverPort))

# listen and only refuse max once
serverSocket.listen(1)
print("TCP Server now listening!")

while 1:
    print("looping again")
    # create a socket specifically for the client that has just requested a connection
    connectionSocket, addr = serverSocket.accept()
    print("new client!")

    # wait whilst trying to receive data from the client on its dedicated connection socket
    client_sentence = connectionSocket.recv(1024)
    client_sentence = client_sentence.decode("utf-8")

    # inspired by: https://stackoverflow.com/questions/39090366/how-to-parse-raw-http-request-in-python-3
    if client_sentence == '':
        continue
    http_req = client_sentence.split("\r\n")
    print(http_req[0])
    wanted_file_name = http_req[0].split(" ")[1][1:]
    print(wanted_file_name)

    http_reply = ''
    print("ATTEMPTING TO OPEN WANTED FILE")
    try:
        wanted_file = open(wanted_file_name)
        http_reply += ("HTTP/1.1 200 OK\r\n")
        file_content = wanted_file.read()
        http_reply += "Content-Length: "
        content_len = len(file_content)
        http_reply += str(content_len)
        http_reply += "\r\n"
        http_reply += "Content-Type: text/html\r\n"
        http_reply += file_content
    except FileNotFoundError: 
        http_reply += "HTTP/1.1 404 Not Found\r\n"
        http_reply += "<html>\n<head>\n<title>404 Not Found</title>\n</head>\n<body>\n<h1>Not Found</h1>\n<p>The file could not be found.</p>\n</body>\n</html>"
        
    print(http_reply)
    connectionSocket.send(str.encode(http_reply))

    connectionSocket.close()