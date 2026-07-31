#ifndef COMUN_H
#define COMUN_H

#define MAX_TRAMA 65536

typedef struct {
    char mensaje_bits[MAX_TRAMA];
    int error_detectado;
    int fue_corregido;
} ResultadoEnlace;

#endif
