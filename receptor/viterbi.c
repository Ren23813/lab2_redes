#include <string.h>
#include <limits.h>
#include "viterbi.h"

#define N_ESTADOS 4
#define MAX_PARES (MAX_TRAMA / 2)

static void transicion(int estado, int b, int *o0, int *o1, int *siguiente) {
    int m1 = estado >> 1;
    int m2 = estado & 1;
    *o0 = b ^ m1 ^ m2;
    *o1 = b ^ m2;
    *siguiente = (b << 1) | m1;
}

ResultadoEnlace decodificar_viterbi(const char *trama) {
    ResultadoEnlace r;
    r.fue_corregido = 0;

    int n_pares = strlen(trama) / 2;
    static int predecesor[MAX_PARES][N_ESTADOS];
    static int bit_entrada[MAX_PARES][N_ESTADOS];
    int metrica[N_ESTADOS], nueva_metrica[N_ESTADOS];

    for (int e = 0; e < N_ESTADOS; e++) metrica[e] = INT_MAX / 2;
    metrica[0] = 0;

    for (int t = 0; t < n_pares; t++) {
        int r0 = trama[2 * t] - '0';
        int r1 = trama[2 * t + 1] - '0';
        for (int e = 0; e < N_ESTADOS; e++) nueva_metrica[e] = INT_MAX / 2;

        for (int prev = 0; prev < N_ESTADOS; prev++) {
            if (metrica[prev] >= INT_MAX / 2) continue;
            for (int b = 0; b <= 1; b++) {
                int o0, o1, siguiente;
                transicion(prev, b, &o0, &o1, &siguiente);
                int costo = metrica[prev] + (o0 != r0) + (o1 != r1);
                if (costo < nueva_metrica[siguiente]) {
                    nueva_metrica[siguiente] = costo;
                    predecesor[t][siguiente] = prev;
                    bit_entrada[t][siguiente] = b;
                }
            }
        }
        memcpy(metrica, nueva_metrica, sizeof(metrica));
    }

    r.error_detectado = (metrica[0] > 0);
    r.fue_corregido = r.error_detectado;

    static int decodificado[MAX_PARES];
    int estado = 0;
    for (int t = n_pares - 1; t >= 0; t--) {
        decodificado[t] = bit_entrada[t][estado];
        estado = predecesor[t][estado];
    }

    int len_mensaje = n_pares - 2;
    for (int i = 0; i < len_mensaje; i++) {
        r.mensaje_bits[i] = '0' + decodificado[i];
    }
    r.mensaje_bits[len_mensaje] = '\0';
    return r;
}
