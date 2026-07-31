def solicitar_mensaje():
    texto = input('Mensaje a enviar: ')
    algoritmo = input('Algoritmo (FLETCHER/VITERBI): ').strip().upper()
    probabilidad = float(input('Probabilidad de error por bit (ej. 0.01): '))
    return texto, algoritmo, probabilidad
