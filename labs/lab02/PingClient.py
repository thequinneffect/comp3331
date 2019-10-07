# using python3
import sys
import socket
from socket import AF_INET, SOCK_DGRAM
from datetime import datetime
import time

# source: https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
current_milli_time = lambda: int(round(time.time() * 1000))

if (len(sys.argv) < 3):
    print("required args: host_ip port")
    exit()

server = sys.argv[1]
port = int(sys.argv[2])

#print(server)
#print(port)

clientSocket = socket.socket(AF_INET, SOCK_DGRAM)
#This line creates the client’s socket. The first parameter indicates the address family; in particular,AF_INET indicates that the underlying network is using IPv4.The second parameter indicates that the socket is of type SOCK_DGRAM,which means it is a UDP socket (rather than a TCP socket, where we use SOCK_STREAM).
clientSocket.settimeout(1)

rtt_times = []
sequence_number = 1
while 1:

    if sequence_number > 10:
        break
    # generate message
    message = "PING " + f"{sequence_number} {datetime.now()}" + "\r\n"

    send_time = current_milli_time()
    # send the message
    clientSocket.sendto(message.encode('utf-8'),(server, port))

    # receive the message back
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    except socket.timeout:
        # print("receiving message back from server timed out")
        print("ping to " + f"{server}" + ", seq =" + f"{sequence_number}" + ", timeout")
        continue

    receive_time = current_milli_time()
    rtt = receive_time - send_time
    rtt_times.append(rtt)

    print("ping to " + f"{server}" + ", seq =" + f"{sequence_number}" + ", rtt = " + f"{rtt}")

    sequence_number += 1

print("minimum rtt: " + f"{min(rtt_times)}")
print("maximum rtt: " + f"{max(rtt_times)}")
print("average rtt: " + f"{sum(rtt_times)/len(rtt_times)}")
clientSocket.close()
# Close the socket