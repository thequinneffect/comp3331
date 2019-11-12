#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <netinet/in.h>
#include <string.h>

#include <arpa/inet.h>
//#include <stdbool.h>

#include <unistd.h>


#define MIN_ARGS 4

#define SERVER_IP "127.0.0.1"

// TODO: make this a helper funtion in a separate file so that client and server can both use it (find what is common between client and server, abstract that)
// void sockaddr_in_init(const uint16_t port);

int main(int argc, char *argv[]) {

    /* check the user supplied the minimum required arguments for the server to run */
    if (argc < MIN_ARGS) {
        printf("usage error: ./server <server_port> <block_duration> <timeout>\n");
        return 0;
    }

    /* extract the arguments */
    if (atoi(argv[1]) > UINT16_MAX || atoi(argv[1]) < 0) {
        printf("usage error: invalid port number, please use a port number in range [0, %d]\n", UINT16_MAX);
    }
    const uint16_t port = atoi(argv[1]);
    const int block_duration = atoi(argv[2]);
    const int timeout_timer = atoi(argv[3]);

    /* set up the server */
    int ssock_fd; // server socket file descriptor
    if ((ssock_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        printf("socket allocation failed\n.");
        return 1;
    }
    struct sockaddr_in ssock_info; // contains info about identifying server (ip addr, port, etc.) - server socket address info
    memset(&ssock_info, 0, sizeof(struct sockaddr_in));
    ssock_info.sin_family = AF_INET; // ipv4
    ssock_info.sin_port = htons(port);
    inet_pton(AF_INET, SERVER_IP, &ssock_info.sin_addr);
    printf("server address in struct: %s:%d\n", inet_ntoa(ssock_info.sin_addr), ntohs(ssock_info.sin_port));

    /* now bind the socket to the port */
    int sockaddr_in_len = sizeof(struct sockaddr_in);
    if (bind(ssock_fd, (struct sockaddr*)&ssock_info, sockaddr_in_len) == -1) {
        printf("socket binding failed!\n");
        return 1;
    }

    /* now listen, with a limit of ... */
    if (listen(ssock_fd, 5) == -1) {
        printf("error trying to listen\n");
    }

    /* enter servicing loop */
    while (1) {

        struct sockaddr_in csock_info;
        int csock_fd;
        if ((csock_fd = accept(ssock_fd, (struct sockaddr*)&csock_info, &sockaddr_in_len)) == -1) {
            printf("server failed to accept new client\n");
        }

        char message[] = "Making contact!\n";
        ssize_t bytes_sent = send(csock_fd, message, strlen(message), 0);

        printf("sent %ld bytes to client: %s:%d\n", bytes_sent, inet_ntoa(csock_info.sin_addr), ntohs(csock_info.sin_port));

        close(csock_fd);
    }
}