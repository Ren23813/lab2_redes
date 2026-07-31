#include <string.h>
#include <stdlib.h>
#include "fletcher.h"

static unsigned long bits_a_entero(const char *bits, int inicio, int len) {
    unsigned long valor = 0;
    for (int i = 0; i < len; i++) {
        valor = (valor << 1) | (bits[inicio + i] - '0');
    }
    return valor;
}

ResultadoEnlace verificar_fletcher(const char *trama, int block_size) {
    ResultadoEnlace r;
    r.fue_corregido = 0;

    int len_total = strlen(trama);
    int len_checksum = 2 * block_size;
    int len_mensaje = len_total - len_checksum;

    memcpy(r.mensaje_bits, trama, len_mensaje);
    r.mensaje_bits[len_mensaje] = '\0';

    unsigned long mod = (1UL << block_size) - 1;
    unsigned long suma_a = 0, suma_b = 0;
    for (int i = 0; i < len_mensaje; i += block_size) {
        unsigned long valor = bits_a_entero(trama, i, block_size);
        suma_a = (suma_a + valor) % mod;
        suma_b = (suma_b + suma_a) % mod;
    }

    unsigned long a_recibido = bits_a_entero(trama, len_mensaje, block_size);
    unsigned long b_recibido = bits_a_entero(trama, len_mensaje + block_size, block_size);

    r.error_detectado = (suma_a != a_recibido || suma_b != b_recibido);
    return r;
}
