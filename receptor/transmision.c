#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include "transmision.h"

void recibir_informacion(int puerto, char *buffer_out, int max_len) {
    int servidor_fd = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(servidor_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in direccion;
    direccion.sin_family = AF_INET;
    direccion.sin_addr.s_addr = INADDR_ANY;
    direccion.sin_port = htons(puerto);

    bind(servidor_fd, (struct sockaddr *) &direccion, sizeof(direccion));
    listen(servidor_fd, 1);
    printf("Escuchando en el puerto %d...\n", puerto);

    int cliente_fd = accept(servidor_fd, NULL, NULL);

    int total = 0;
    while (total < max_len - 1) {
        int leidos = recv(cliente_fd, buffer_out + total, max_len - 1 - total, 0);
        if (leidos <= 0) break;
        total += leidos;
        if (buffer_out[total - 1] == '\n') break;
    }
    buffer_out[total] = '\0';
    if (total > 0 && buffer_out[total - 1] == '\n') buffer_out[total - 1] = '\0';

    close(cliente_fd);
    close(servidor_fd);
}
