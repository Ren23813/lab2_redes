#include <string.h>
#include "presentacion.h"

void decodificar_mensaje(const char *bits, char *texto_out) {
    int len = strlen(bits);
    int n_chars = len / 8;
    for (int i = 0; i < n_chars; i++) {
        int valor = 0;
        for (int j = 0; j < 8; j++) {
            valor = (valor << 1) | (bits[i * 8 + j] - '0');
        }
        texto_out[i] = (char) valor;
    }
    texto_out[n_chars] = '\0';
}
