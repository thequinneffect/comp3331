#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdbool.h>

#define MIN_ARGS 3
#define LOCALHOST_IP "127.0.0.1"
#define MAX_INPUT 256

int main(int argc, char* argv[]) {

    /* check the user supplied the minimum required arguments for the client to run */
    if (argc < MIN_ARGS) {
        printf("usage error: ./client <server_ip> <server_port>\n");
        return 0;
    }

    /* extract the arguments */
    if (atoi(argv[2]) > UINT16_MAX || atoi(argv[1]) < 0) {
        printf("usage error: invalid port number, please use a port number in range [0, %d]\n", UINT16_MAX);
    }
    char server_address[strlen(argv[1])];
    strcpy(server_address, argv[1]);
    printf("server address is: %s\n", server_address);
    if (!strcmp(server_address, "localhost")) {                              // "127.0.0.1\0"
        strcpy(server_address, LOCALHOST_IP); // guaranteed enough space because "localhost\0"
        printf("server address changed to: %s\n", server_address);
    }
    const uint16_t server_port = atoi(argv[2]);
    printf("server port is: %u\n", server_port);

    /* set up connection details of remote servers socket */
    struct sockaddr_in server_info;
    memset(&server_info, 0, sizeof(struct sockaddr_in));
    server_info.sin_family = AF_INET;
    inet_pton(AF_INET, server_address, &server_info.sin_addr);
    server_info.sin_port = htons(server_port);
    printf("server address in struct: %s:%d\n", inet_ntoa(server_info.sin_addr), ntohs(server_info.sin_port));

    /* now open up a local socket for the client */
    int client_fd;
    if ((client_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        printf("socket allocation failed\n.");
        return 1;
    }

    /* try connect to the server */
    if (connect(client_fd, (const struct sockaddr*)&server_info, sizeof(struct sockaddr_in)) == -1) {
        printf("error: coudln't connect to server %s:%d\n", inet_ntoa(server_info.sin_addr), server_info.sin_port);
    }   

    char username[MAX_INPUT] = {0};
    char password[MAX_INPUT] = {0};
    printf("username: ");
    fgets(username, MAX_INPUT, stdin);
    username[strcspn(username, "\n")] = '\0'; // replace newline with null char
    printf("username is: %s (should be no newline)\n", username);
    printf("password: ");
    fgets(password, MAX_INPUT, stdin);
    password[strcspn(password, "\n")] = '\0'; // replace newline with null char
    printf("password is: %s (should be no newline)\n", password);

    send(client_fd, username, strlen(username), 0);

    char response[MAX_INPUT] = {0};
    recv(client_fd, response, MAX_INPUT, 0);

    printf("server responded with: %s\n", response);
}