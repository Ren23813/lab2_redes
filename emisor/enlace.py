from fletcher import calcular_fletcher
from viterbi import codificar_viterbi


def calcular_integridad(bits, algoritmo, block_size=16):
    if algoritmo == 'FLETCHER':
        bits_padded, checksum = calcular_fletcher(bits, block_size)
        trama = bits_padded + checksum
        parametro = str(block_size)
    elif algoritmo == 'VITERBI':
        trama = codificar_viterbi(bits)
        parametro = '0'
    else:
        raise ValueError('Algoritmo no soportado: ' + algoritmo)

    return trama, parametro
