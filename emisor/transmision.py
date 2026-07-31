import socket


def enviar_informacion(host, puerto, mensaje):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, puerto))
        s.sendall(mensaje.encode('utf-8') + b'\n')
