import sys
import random
import socket


def aplicar_ruido(bits, probabilidad):
    resultado = []
    for bit in bits:
        if random.random() < probabilidad:
            resultado.append('1' if bit == '0' else '0')
        else:
            resultado.append(bit)
    return ''.join(resultado)



def calcular_fletcher(bits, block_size):
    padding = (-len(bits)) % block_size
    bits_padded = bits + '0' * padding

    mod = (1 << block_size) - 1
    suma_a, suma_b = 0, 0
    for i in range(0, len(bits_padded), block_size):
        valor = int(bits_padded[i:i + block_size], 2)
        suma_a = (suma_a + valor) % mod
        suma_b = (suma_b + suma_a) % mod

    checksum = format(suma_a, '0{}b'.format(block_size)) + format(suma_b, '0{}b'.format(block_size))
    return bits_padded, checksum




def codificar_mensaje(texto):
    return ''.join(format(ord(c), '08b') for c in texto)


def codificar_viterbi(bits):
    bits_flush = bits + '00'
    m1, m2 = 0, 0
    salida = []
    for c in bits_flush:
        b = int(c)
        o0 = b ^ m1 ^ m2
        o1 = b ^ m2
        salida.append(str(o0))
        salida.append(str(o1))
        m1, m2 = b, m1
    return ''.join(salida)



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

def solicitar_mensaje():
    texto = input('Mensaje a enviar: ')
    algoritmo = input('Algoritmo (FLETCHER/VITERBI): ').strip().upper()
    probabilidad = float(input('Probabilidad de error por bit (ej. 0.01): '))
    return texto, algoritmo, probabilidad

def enviar_informacion(host, puerto, mensaje):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, puerto))
        s.sendall(mensaje.encode('utf-8') + b'\n')



HOST = '127.0.0.1'
PUERTO = 6000
BLOCK_SIZE = 16


def main():
    if len(sys.argv) == 4:
        texto, algoritmo, probabilidad = sys.argv[1], sys.argv[2].upper(), float(sys.argv[3])
    else:
        texto, algoritmo, probabilidad = solicitar_mensaje()

    bits = codificar_mensaje(texto)
    trama, parametro = calcular_integridad(bits, algoritmo, BLOCK_SIZE)
    trama_con_ruido = aplicar_ruido(trama, probabilidad)

    mensaje_socket = '{}:{}:{}'.format(algoritmo, parametro, trama_con_ruido)
    enviar_informacion(HOST, PUERTO, mensaje_socket)
    print('Enviado: {} bits ({} bits de carga + redundancia)'.format(len(trama_con_ruido), len(bits)))


if __name__ == '__main__':
    main()
