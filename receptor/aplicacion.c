#include <stdio.h>
#include <string.h>
#include "aplicacion.h"

void mostrar_mensaje(const char *algoritmo, ResultadoEnlace r, const char *texto) {
    if (strcmp(algoritmo, "FLETCHER") == 0 && r.error_detectado) {
        printf("ERROR: se detectaron errores y el algoritmo no puede corregirlos.\n");
        return;
    }
    if (strcmp(algoritmo, "VITERBI") == 0 && r.fue_corregido) {
        printf("(se detectaron y corrigieron errores de transmision)\n");
    }
    printf("Mensaje recibido: %s\n", texto);
}
