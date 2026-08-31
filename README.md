# Laboratorio 1: Filtración de Datos vía ICMP (Modo Stealth) 🕵️‍♂️

Este repositorio contiene el código y los archivos necesarios para replicar una prueba de concepto de filtración de datos (exfiltración) utilizando paquetes ICMP (ping). El objetivo es ocultar un mensaje cifrado dentro del payload de paquetes ICMP Echo Request para evadir sistemas de Deep Packet Inspection (DPI), y posteriormente extraerlo mediante un ataque Man-in-the-Middle (MitM).

## 🛠️ Requisitos Previos

- **Sistema Operativo:** Linux (recomendado) o macOS.
- **Software:** 
  - Python 3.x
  - Wireshark
  - Librería `scapy` (`pip install scapy`)
- **Permisos:** Privilegios de administrador (`sudo`) para capturar tráfico e inyectar paquetes.

---

## 🚀 Guía Paso a Paso para Replicar el Laboratorio

### Fase 1: Preparación y Captura de Tráfico

1. **Abrir Wireshark en modo Loopback:**
   - Abre Wireshark (si no ves las interfaces, ejecútalo desde la terminal con `sudo wireshark`).
   - Busca la interfaz **`Loopback: lo`** (en Linux) y haz doble clic para comenzar a capturar tráfico.
   
2. **Aplicar filtro ICMP:**
   - En la barra superior de filtros (donde dice *Apply a display filter*), escribe `icmp` y presiona **Enter**. 
   - *Nota: Esto no detiene la captura de otros paquetes, solo limpia la vista para mostrar únicamente el tráfico ICMP.*

### Fase 2: Generación de Tráfico (Real vs. Stealth)

3. **Capturar tráfico real (ANTES):**
   - Abre una terminal (sin cerrar Wireshark) y ejecuta un ping estándar:
     ```bash
     ping -c 3 127.0.0.1
     ```
   - Verás en Wireshark 3 pares de *Echo Request/Echo Reply*. Esta es tu referencia de tráfico legítimo.

4. **Ejecutar el script Stealth:**
   - En la misma terminal, ejecuta el script de envío con el mensaje cifrado (ej. "KrodPxqgr" corresponde a "HolaMundo" con corrimiento 3):
     ```bash
     sudo python3 stealth_icmp.py 127.0.0.1 "KrodPxqgr"
     ```
   - Verás aparecer en Wireshark un paquete por cada carácter del mensaje.

5. **Capturar tráfico real (DESPUÉS):**
   - Apenas termine el script, vuelve a ejecutar el ping estándar:
     ```bash
     ping -c 3 127.0.0.1
     ```
   - Con esto cerramos el ciclo, obteniendo una captura continua con 3 tramos: `Ping Real -> Tráfico Stealth -> Ping Real`.

6. **Guardar la captura:**
   - En Wireshark, haz clic en el botón rojo (Stop capturing) en la esquina superior izquierda.
   - Ve a **File > Save As**, nombra el archivo como `captura_lab1.pcapng` y guárdalo en la carpeta de este repositorio.

### Fase 3: Análisis Visual en Wireshark

7. **Identificar los paquetes:**
   - En la lista de paquetes (*Packet List*), identifica los tres tramos:
     - **Primer bloque:** Ping real (ID asignado por el sistema, ej. `0x7a7a`).
     - **Segundo bloque:** Nuestro tráfico (ID fijo `0x1234` o su equivalente en bytes invertidos mostrado en Wireshark).
     - **Tercer bloque:** Ping real nuevamente.

8. **Comparación de Payload (Data):**
   - Selecciona un paquete real, expande **Internet Control Message Protocol > Data** y observa el hexdump. El tamaño total del payload es de 56 bytes.
   - Selecciona un paquete stealth y repite el proceso. 
   - **🔍 Observación clave:** En el paquete stealth, podrás notar que el tamaño del payload cuadra (56 bytes), pero en la posición 8 (justo después de los 8 bytes de nuestro timestamp) se encuentra inyectado el carácter cifrado.

### Fase 4: Extracción MitM y Descifrado

9. **Ejecutar el script MitM:**
   - En la terminal, corre el script de extracción pasándole el archivo capturado:
     ```bash
     python3 mitm_icmp.py captura_lab1.pcapng
     ```
   - *Solución de problemas:* Si Scapy arroja error al leer el `.pcapng`, vuelve a Wireshark y exporta el archivo como **`Wireshark/tcpdump - pcap`** tradicional y usa ese archivo.

10. **Verificar Resultados:**
    - El script filtrará automáticamente los paquetes con `ID=0x1234`.
    - Extraerá el payload, reconstruirá el mensaje cifrado (`KrodPxqgr`) y probará por fuerza bruta los 26 desplazamientos del cifrado César.
    - Mediante análisis de frecuencias en español, el programa resaltará **en color verde** el desplazamiento correcto, revelando el mensaje original: `HolaMundo`.

---

## 📂 Estructura de Archivos

- `cesar.py`: Script para cifrar un texto usando el algoritmo César.
- `stealth_icmp.py`: Script que inyecta y envía el texto cifrado a través de paquetes ICMP simulando un ping legítimo.
- `mitm_icmp.py`: Script que lee un archivo `.pcap`, extrae el mensaje oculto y lo rompe por fuerza bruta.
- `captura_lab1.pcapng`: Archivo de captura de tráfico de ejemplo.
- `README.md`: Este archivo.
