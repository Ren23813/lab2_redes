#include <string.h>
#include "enlace.h"
#include "fletcher.h"
#include "viterbi.h"

ResultadoEnlace procesar_enlace(const char *algoritmo, int parametro, const char *trama) {
    if (strcmp(algoritmo, "FLETCHER") == 0) {
        return verificar_fletcher(trama, parametro);
    }
    return decodificar_viterbi(trama);
}
