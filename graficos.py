import random
import matplotlib.pyplot as plt
from emisor.main_emisor import codificar_mensaje, aplicar_ruido





def decodificar_mensaje(bits):
    chars = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)



# Fletcher (misma logica que fletcher.c) 

def fletcher_calcular(bits, block_size):
    padding = (-len(bits)) % block_size
    bits = bits + '0' * padding
    mod = (1 << block_size) - 1
    a, b = 0, 0
    for i in range(0, len(bits), block_size):
        a = (a + int(bits[i:i + block_size], 2)) % mod
        b = (b + a) % mod
    return bits, format(a, '0{}b'.format(block_size)) + format(b, '0{}b'.format(block_size))


def fletcher_verificar(trama, block_size):
    len_checksum = 2 * block_size
    mensaje, checksum_recibido = trama[:-len_checksum], trama[-len_checksum:]
    _, checksum_calculado = fletcher_calcular(mensaje, block_size)
    return checksum_calculado == checksum_recibido, mensaje


#  Viterbi (misma logica que algoritmos.c) 

def viterbi_codificar(bits):
    bits = bits + '00'
    m1, m2, salida = 0, 0, []
    for c in bits:
        b = int(c)
        salida.append(str(b ^ m1 ^ m2))
        salida.append(str(b ^ m2))
        m1, m2 = b, m1
    return ''.join(salida)


def _transicion(estado, b):
    m1, m2 = estado >> 1, estado & 1
    o0, o1 = b ^ m1 ^ m2, b ^ m2
    return o0, o1, (b << 1) | m1


def viterbi_decodificar(trama):
    n_pares = len(trama) // 2
    INF = float('inf')
    metrica = [0, INF, INF, INF]
    predecesor = [[0] * 4 for _ in range(n_pares)]
    bit_entrada = [[0] * 4 for _ in range(n_pares)]

    for t in range(n_pares):
        r0, r1 = int(trama[2 * t]), int(trama[2 * t + 1])
        nueva = [INF] * 4
        for prev in range(4):
            if metrica[prev] == INF:
                continue
            for b in (0, 1):
                o0, o1, sig = _transicion(prev, b)
                costo = metrica[prev] + (o0 != r0) + (o1 != r1)
                if costo < nueva[sig]:
                    nueva[sig] = costo
                    predecesor[t][sig] = prev
                    bit_entrada[t][sig] = b
        metrica = nueva

    decodificado = [0] * n_pares
    estado = 0
    for t in range(n_pares - 1, -1, -1):
        decodificado[t] = bit_entrada[t][estado]
        estado = predecesor[t][estado]

    bits = ''.join(str(b) for b in decodificado[:-2])
    return bits


# ---------- Simulacion 1: tasa de exito vs probabilidad de error ----------

def simular_exito(mensaje, algoritmo, probabilidad, n_pruebas, block_size=16):
    bits = codificar_mensaje(mensaje)
    exitos = 0
    for _ in range(n_pruebas):
        if algoritmo == 'FLETCHER':
            _, checksum = fletcher_calcular(bits, block_size)
            trama = bits + checksum
            padding = (-len(bits)) % block_size
            trama_ruido = aplicar_ruido(trama, probabilidad)
            ok, mensaje_bits = fletcher_verificar(trama_ruido, block_size)
            recuperado = ok and decodificar_mensaje(mensaje_bits[:len(bits)]) == mensaje
        else:
            trama = viterbi_codificar(bits)
            trama_ruido = aplicar_ruido(trama, probabilidad)
            mensaje_bits = viterbi_decodificar(trama_ruido)
            recuperado = decodificar_mensaje(mensaje_bits) == mensaje
        exitos += recuperado
    return exitos / n_pruebas * 100


mensaje_prueba = "Redes de Computadoras UVG"
probabilidades = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20]
N_PRUEBAS = 300

resultados_fletcher = [simular_exito(mensaje_prueba, 'FLETCHER', p, N_PRUEBAS) for p in probabilidades]
resultados_viterbi = [simular_exito(mensaje_prueba, 'VITERBI', p, N_PRUEBAS) for p in probabilidades]

plt.figure(figsize=(7, 5))
plt.plot([p * 100 for p in probabilidades], resultados_fletcher, marker='o', label='Fletcher (deteccion)')
plt.plot([p * 100 for p in probabilidades], resultados_viterbi, marker='s', label='Viterbi (correccion)')
plt.xlabel('Probabilidad de error por bit (%)')
plt.ylabel('Mensajes recuperados correctamente (%)')
plt.title('Tasa de exito vs. probabilidad de error de canal\n(mensaje de {} caracteres, {} pruebas por punto)'.format(len(mensaje_prueba), N_PRUEBAS))
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafica_tasa_exito.png', dpi=150)
plt.close()

# ---------- Simulacion 2: overhead vs tamano del mensaje ----------

tamanos = [1, 5, 10, 20, 40, 80, 160, 320]
overhead_fletcher_16 = []
overhead_viterbi = []

for n in tamanos:
    bits_len = n * 8
    checksum_bits = 2 * 16
    overhead_fletcher_16.append(checksum_bits / bits_len * 100)
    overhead_viterbi.append(((bits_len + 2) * 2 - bits_len) / bits_len * 100)

plt.figure(figsize=(7, 5))
plt.plot(tamanos, overhead_fletcher_16, marker='o', label='Fletcher (bloque=16 bits)')
plt.plot(tamanos, overhead_viterbi, marker='s', label='Viterbi (tasa 1/2)')
plt.xlabel('Tamano del mensaje (caracteres)')
plt.ylabel('Overhead (% de bits extra sobre el mensaje)')
plt.title('Overhead de redundancia vs. tamano del mensaje')
plt.xscale('log')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafica_overhead.png', dpi=150)
plt.close()

print('Listo. Datos tasa de exito:')
for p, f, v in zip(probabilidades, resultados_fletcher, resultados_viterbi):
    print('  p={:.2f} -> Fletcher={:.1f}%  Viterbi={:.1f}%'.format(p, f, v))

# ---------- Simulacion 3: tasa de exito vs tamano del mensaje (prob. fija) ----------

def mensaje_de_longitud(n):
    base = "este es un mensaje de prueba para el laboratorio de redes "
    while len(base) < n:
        base += base
    return base[:n]

PROB_FIJA = 0.05
tamanos_mensaje = [4, 13, 25, 40, 63, 90, 130]
exito_viterbi_por_tamano = []
exito_fletcher_por_tamano = []

for n in tamanos_mensaje:
    msg = mensaje_de_longitud(n)
    exito_viterbi_por_tamano.append(simular_exito(msg, 'VITERBI', PROB_FIJA, N_PRUEBAS))
    exito_fletcher_por_tamano.append(simular_exito(msg, 'FLETCHER', PROB_FIJA, N_PRUEBAS))

plt.figure(figsize=(7, 5))
plt.plot(tamanos_mensaje, exito_viterbi_por_tamano, marker='s', label='Viterbi (correccion)')
plt.plot(tamanos_mensaje, exito_fletcher_por_tamano, marker='o', label='Fletcher (deteccion)')
plt.xlabel('Tamano del mensaje (caracteres)')
plt.ylabel('Mensajes recuperados correctamente (%)')
plt.title('Tasa de exito vs. tamano del mensaje\n(probabilidad de error fija = {:.0f}%, {} pruebas por punto)'.format(PROB_FIJA*100, N_PRUEBAS))
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafica_exito_vs_tamano.png', dpi=150)
plt.close()

print('Tasa de exito vs tamano (p={:.0f}%):'.format(PROB_FIJA*100))
for n, v, f in zip(tamanos_mensaje, exito_viterbi_por_tamano, exito_fletcher_por_tamano):
    print('  {} chars -> Viterbi={:.1f}%  Fletcher={:.1f}%'.format(n, v, f))