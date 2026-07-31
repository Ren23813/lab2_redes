import random


def aplicar_ruido(bits, probabilidad):
    resultado = []
    for bit in bits:
        if random.random() < probabilidad:
            resultado.append('1' if bit == '0' else '0')
        else:
            resultado.append(bit)
    return ''.join(resultado)
