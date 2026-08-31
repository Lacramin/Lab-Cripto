# Laboratorio 1: Filtración de Datos vía ICMP (Modo Stealth)

Este repositorio contiene el código y los archivos para replicar una prueba de concepto de filtración de datos (exfiltración) mediante paquetes ICMP (ping). El objetivo es ocultar un mensaje cifrado en el payload de un paquete ICMP Echo Request para evadir sistemas de Deep Packet Inspection (DPI), y luego extraerlo mediante un ataque Man-in-the-Middle (MitM).

## Requisitos

- **Sistema Operativo:** Linux (recomendado) o macOS.
- **Software:** Python 3.x, Wireshark, librería `scapy` (`pip install scapy`).
- **Permisos:** Privilegios de administrador (`sudo`) para captura e inyección de paquetes.

---

## Guía de uso

### 1. Preparación y captura

1. Abre Wireshark (con `sudo` si es necesario) y selecciona la interfaz `Loopback: lo` para iniciar la captura de tráfico.
2. Aplica el filtro `icmp` en la barra superior. Esto solo limpia la vista, la captura de fondo sigue activa guardando todo.

### 2. Generación de tráfico

3. Abre una terminal y ejecuta un ping estándar para generar tráfico de referencia (el "antes"):
   ```bash
   ping -c 3 127.0.0.1
