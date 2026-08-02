#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include "algoritmos.h"

// Capa de transmision 
static void recibir_informacion(int puerto, char *buffer_out, int max_len) {
    int servidor_fd = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(servidor_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in direccion = {0};
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


// Capa de presentacion (binario a ASCII)
static void decodificar_mensaje(const char *bits, char *texto_out) {
    int n_chars = strlen(bits) / 8;
    for (int i = 0; i < n_chars; i++) {
        int valor = 0;
        for (int j = 0; j < 8; j++) valor = (valor << 1) | (bits[i * 8 + j] - '0');
        texto_out[i] = (char) valor;
    }
    texto_out[n_chars] = '\0';
}

// Capa de enlace
static ResultadoEnlace procesar_enlace(const char *algoritmo, int parametro, const char *trama) {
    if (strcmp(algoritmo, "FLETCHER") == 0) return verificar_fletcher(trama, parametro);
    return decodificar_viterbi(trama);
}


// Capa de aplicacion
static void mostrar_mensaje(const char *algoritmo, ResultadoEnlace r, const char *texto) {
    if (strcmp(algoritmo, "FLETCHER") == 0 && r.error_detectado) {
        printf("ERROR: se detectaron errores y el algoritmo no puede corregirlos.\n");
        return;
    }
    if (strcmp(algoritmo, "VITERBI") == 0 && r.fue_corregido) {
        printf("(se detectaron y corrigieron errores de transmision)\n");
    }
    printf("Mensaje recibido: %s\n", texto);
}


            // MAIN
int main(int argc, char *argv[]) {
    int puerto = (argc > 1) ? atoi(argv[1]) : 6000;

    static char buffer[MAX_TRAMA];
    recibir_informacion(puerto, buffer, MAX_TRAMA);

    char algoritmo[32];
    int parametro;
    char *trama = strchr(strchr(buffer, ':') + 1, ':') + 1;
    sscanf(buffer, "%31[^:]:%d:", algoritmo, &parametro);

    ResultadoEnlace r = procesar_enlace(algoritmo, parametro, trama);

    static char texto[MAX_TRAMA / 8 + 1];
    decodificar_mensaje(r.mensaje_bits, texto);

    mostrar_mensaje(algoritmo, r, texto);
    return 0;
}
