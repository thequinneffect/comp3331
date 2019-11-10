#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>


int main(int argc, char* argv[])
{
    int sock_fd, client_fd; // the fd we will use to interact with our socket (everything is a file - linux) (same for client)
    struct sockaddr_in server, client; // the structs that contain information about identifying our server and client (ip address and port numbers)

    /* try and allocate a ipv4, tcp, ?protocol socket */
    if ((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        printf("socket allocation failed\n.");
        return 1;
    }

    /* fill out the server details */
    server.sin_family = AF_INET; // ipv4
    //printf("size of server.sin_family is: %lu\n", sizeof(server.sin_family));
    server.sin_port = htons(12000); // port 12000, this is a short and so has to be converted to network byte order, big endian
    //printf("size of server.sin_port is: %lu\n", sizeof(server.sin_port));
    server.sin_addr.s_addr = INADDR_ANY; // bind to all ip interfaces on this machine (wifi and ethernet + any others)
    //printf("size of server.sin_addr.s_addr is: %lu\n", sizeof(server.sin_addr.s_addr));
    bzero(&server.sin_zero, 8); // size of above fields are 2, 2, 4 bytes, so after 8 zero out the rest of the struct

    int sockaddr_in_len = sizeof(struct sockaddr_in);
    /* now bind the socket to the port */
    if (bind(sock_fd, (struct sockaddr*)&server, sockaddr_in_len) == -1)
    {
        printf("socket binding failed!\n");
        return 1;
    }

    if (listen(sock_fd, 5) == -1)
    {
        printf("error trying to listen\n");
    }

    while (1)
    {

        if ((client_fd = accept(sock_fd, (struct sockaddr*)&client, &sockaddr_in_len)) == -1)
        {
            printf("server failed to accept new client\n");
        }

        char message[] = "Welcome to my TCP server!\n";
        ssize_t bytes_sent = send(client_fd, message, strlen(message), 0);

        printf("sent %ld bytes to client: %s\n", bytes_sent, inet_ntoa(client.sin_addr));

        close(client_fd);
    }
}
