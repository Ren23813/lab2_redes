#ifndef ALGORITMOS_H
#define ALGORITMOS_H

#define MAX_TRAMA 65536

typedef struct {
    char mensaje_bits[MAX_TRAMA];
    int error_detectado;
    int fue_corregido;
} ResultadoEnlace;

ResultadoEnlace verificar_fletcher(const char *trama, int block_size);
ResultadoEnlace decodificar_viterbi(const char *trama);

#endif
