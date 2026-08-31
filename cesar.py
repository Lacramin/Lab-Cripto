#!/usr/bin/env python3
import argparse

def cifrar_cesar(texto, desplazamiento):
    resultado = []
    for c in texto:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            resultado.append(chr((ord(c) - base + desplazamiento) % 26 + base))
        else:
            resultado.append(c)
    return ''.join(resultado)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cifrado César")
    parser.add_argument("texto", help="Texto a cifrar")
    parser.add_argument("desplazamiento", type=int, help="Número de posiciones a desplazar")
    args = parser.parse_args()
    print(cifrar_cesar(args.texto, args.desplazamiento))
