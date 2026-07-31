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
