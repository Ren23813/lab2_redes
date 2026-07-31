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
