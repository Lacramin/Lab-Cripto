#!/usr/bin/env python3
import sys
from scapy.all import rdpcap, ICMP, IP
from collections import Counter

FREC_ESP = {
    'a': 12.53, 'b': 1.42, 'c': 4.68, 'd': 5.86, 'e': 13.68,
    'f': 0.69, 'g': 1.01, 'h': 0.70, 'i': 6.25, 'j': 0.44,
    'k': 0.02, 'l': 4.97, 'm': 3.15, 'n': 6.71, 'ñ': 0.31,
    'o': 8.68, 'p': 2.51, 'q': 0.88, 'r': 6.87, 's': 7.98,
    't': 4.63, 'u': 3.93, 'v': 0.90, 'w': 0.02, 'x': 0.22,
    'y': 0.90, 'z': 0.52
}

ID_ICMP = 0x1234
POSICION_INYECCION = 8

def descifrar_cesar(texto, desplazamiento):
    resultado = []
    for c in texto:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            resultado.append(chr((ord(c) - base - desplazamiento) % 26 + base))
        else:
            resultado.append(c)
    return ''.join(resultado)

def puntuar_texto(texto):
    letras = [c.lower() for c in texto if c.isalpha()]
    if not letras:
        return float('inf')
    total = len(letras)
    frec = Counter(letras)
    puntaje = 0
    for letra, count in frec.items():
        if letra in FREC_ESP:
            esperado = FREC_ESP[letra] / 100.0
            observado = count / total
            puntaje += (observado - esperado) ** 2
    return puntaje

def extraer_mensaje(pcap_file, ip_origen=None):
    paquetes = rdpcap(pcap_file)
    mensaje = []
    for pkt in paquetes:
        if ICMP in pkt and pkt[ICMP].type == 8 and pkt[ICMP].id == ID_ICMP:
            if ip_origen and (IP not in pkt or pkt[IP].src != ip_origen):
                continue
            payload = bytes(pkt[ICMP].payload)
            if len(payload) > POSICION_INYECCION:
                byte = payload[POSICION_INYECCION]
                try:
                    caracter = chr(byte)
                    if caracter.isprintable():
                        mensaje.append(caracter)
                    else:
                        mensaje.append('?')
                except:
                    mensaje.append('?')
    return ''.join(mensaje)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Uso: python3 mitm_icmp_final.py <archivo.pcap> [IP_origen]")
        print("  Si no se especifica IP_origen, se procesan todos los paquetes ICMP con ID 0x1234.")
        sys.exit(1)

    archivo = sys.argv[1]
    ip_origen = sys.argv[2] if len(sys.argv) == 3 else None

    texto_cifrado = extraer_mensaje(archivo, ip_origen)

    if not texto_cifrado:
        print("No se encontraron paquetes ICMP Echo Request con ID 0x1234 y payload suficiente.")
        print("Verifica que el archivo .pcap contenga paquetes de tu script o especifica la IP origen.")
        sys.exit(1)

    print(f"\nMensaje cifrado reconstruido: {texto_cifrado}\n")

    resultados = []
    for shift in range(26):
        texto_plano = descifrar_cesar(texto_cifrado, shift)
        puntaje = puntuar_texto(texto_plano)
        resultados.append((shift, texto_plano, puntaje))

    mejor_puntaje = min(r[2] for r in resultados)

    print("Posibles mensajes (desplazamiento -> texto):")
    for shift, texto, punt in resultados:
        if punt == mejor_puntaje:
            print(f"\033[92mDesplazamiento {shift:2d}: {texto}\033[0m")
        else:
            print(f"Desplazamiento {shift:2d}: {texto}")
    print("\n(El texto en verde es el más probable según análisis de frecuencia.)")
