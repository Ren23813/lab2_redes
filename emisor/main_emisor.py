import sys
from aplicacion import solicitar_mensaje
from presentacion import codificar_mensaje
from enlace import calcular_integridad
from ruido import aplicar_ruido
from transmision import enviar_informacion

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
