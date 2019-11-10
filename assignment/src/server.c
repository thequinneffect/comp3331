//#include <arpa/inet.h>
//#include <netinet/in.h>
//#include <stdbool.h>
#include <stdio.h>
//#include <string.h>
//#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>

#define MIN_ARGS 4

int main(int argc, char *argv[])
{
    /* check the user supplied the minimum required arguments for the server to run */
    if (argc < MIN_ARGS) {
        printf("usage error: ./server <server_port> <block_duration> <timeout>\n");
        return 0;
    }

    printf("setting up server\n");
    if (atoi(argv[1]) > UINT16_MAX || atoi(argv[1]) < 0) {
        printf("usage error: invalid port number, please use a port number in range [0, %d]\n", UINT16_MAX);
    }
    uint16_t server_port = atoi(argv[1]);

}