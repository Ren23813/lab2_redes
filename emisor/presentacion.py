def codificar_mensaje(texto):
    return ''.join(format(ord(c), '08b') for c in texto)
