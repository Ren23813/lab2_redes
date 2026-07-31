#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "comun.h"
#include "transmision.h"
#include "enlace.h"
#include "presentacion.h"
#include "aplicacion.h"

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
