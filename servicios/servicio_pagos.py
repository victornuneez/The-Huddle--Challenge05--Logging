
"""
Este es un ervicio simulado de procesamiento de pagos que genera logs

Simula estos eventos:
- Pagos procesados exitosamente
- Rechazos de tarjetas
- Verificaciones de fraude
- Errores de conexión con bancos
"""

import requests
import random
from datetime import datetime
import time

# ==========================
# CONFIGURACIÓN DEL SERVICIO
# ==========================

NOMBRE_SERVICIO = "PaymentService"
TOKEN = "Token PAYMENT_SERVICE_2024"
URL_SERVIDOR = "http://localhost:5000/logs"

INTERVALO_MIN = 2
INTERVALO_MAX = 6

# =================================
# DATOS PARA GENERAR LOGS REALISTAS
# =================================

niveles = ["INFO", "WARNING", "ERROR", "CRITICAL"]

mensajes_por_nivel = {
    "INFO": [
        "Pago procesado exitosamente - Monto: $150.00",
        "Reembolso realizado correctamente",
        "Tarjeta verificada y aprobada",
        "Transacción completada sin problemas",
        "Confirmación de pago enviada al usuario"
    ],
    "WARNING": [
        "Tarjeta cerca de fecha de expiración",
        "Detección de patrón inusual de compra",
        "Límite de crédito próximo a alcanzarse",
        "Intento de pago duplicado detectado",
        "Dirección de facturación no coincide"
    ],
    "ERROR": [
        "Pago rechazado - Fondos insuficientes",
        "Tarjeta reportada como robada",
        "CVV inválido proporcionado",
        "Timeout al procesar transacción con banco"
    ],
    "CRITICAL": [
        "Servicio de pagos completamente caído",
        "Pérdida de conexión con todos los bancos",
        "Fallo crítico en validación de transacciones",
        "Sistema de detección de fraude no responde",
        "Base de datos de transacciones inaccesible"
    ]
}

# =====================================
# FUNCIÓN PARA GENERAR UN LOG ALEATORIO
# =====================================

# Genera un log aleatorio del servicio de pagos
def generar_log():
    nivel = random.choice(niveles)
    mensaje = random.choice(mensajes_por_nivel[nivel])
    
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service": NOMBRE_SERVICIO,
        "severity": nivel,
        "message": mensaje
    }
    
    return log


# ===================================
# FUNCIÓN PARA ENVIAR LOG AL SERVIDOR
# ===================================

# Envía un log al servidor central
def enviar_log(log):
    """Envía un log al servidor central"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": TOKEN
        }
        
        respuesta = requests.post(URL_SERVIDOR, json=log, headers=headers, timeout=5)
        
        if respuesta.status_code == 201:
            print(f"Log enviado: [{log['severity']}] {log['message'][:50]}")
            return True
        else:
            print(f"Error {respuesta.status_code}: {respuesta.text}")
            return False
            

    except Exception as error:
        print(f"Error: {error}")
        return False

# ================================
# BUCLE PARA GENERAR Y ENVIAR LOGS
# ================================

# Bucle principal que genera y envía logs.
def ejecutar_servicio():
    print("=" * 70)
    print(f"{NOMBRE_SERVICIO} INICIADO")
    print("=" * 70)
    print(f"Servidor destino: {URL_SERVIDOR}")
    print(f"Token: {TOKEN}")
    print(f"Intervalo: {INTERVALO_MIN}-{INTERVALO_MAX} segundos")
    print(f"Presiona Ctrl+C para detener")
    print("=" * 70 + "\n")
    
    contador = 0
    
    try:
        while True:
            contador += 1
            
            log = generar_log()
            
            print(f"\nEnviando log #{contador}")
            enviar_log(log)
            print()
            
            espera = random.randint(INTERVALO_MIN, INTERVALO_MAX)
            print(f"Esperando {espera} segundos")
            time.sleep(espera)
            
    except KeyboardInterrupt:
        print(f"\n{'='*70}")
        print(f"{NOMBRE_SERVICIO} DETENIDO")
        print(f"Total de logs enviados: {contador}")
        print("="*70)


# Sirve para que solo se ejecute este script completo solo si se ejecuta directamente, evita que este servicio se ejecute automaticamente cuando es importado.
if __name__ == "__main__":
    ejecutar_servicio()