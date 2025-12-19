
"""
Este servicio simula el envío de emails que genera logs

Simula estos eventos:
- Emails enviados exitosamente
- Errores de servidor SMTP
- Detección de spam
- Problemas de conectividad
"""

import requests
import random
from datetime import datetime
import time

# ==========================
# CONFIGURACIÓN DEL SERVICIO
# ==========================

NOMBRE_SERVICIO = "EmailService"
TOKEN = "Token EMAIL_SERVICE_2024"
URL_SERVIDOR = "http://localhost:5000/logs"

INTERVALO_MIN = 4
INTERVALO_MAX = 8

# =================================
# DATOS PARA GENERAR LOGS REALISTAS
# =================================

niveles = ["INFO", "WARNING", "ERROR", "DEBUG"]

mensajes_por_nivel = {
    "INFO": [
        "Email de bienvenida enviado correctamente",
        "Confirmación de registro entregada",
        "Email de recuperación de contraseña enviado",
        "Notificación de compra entregada exitosamente"
    ],
    "WARNING": [
        "Email marcado como spam por el servidor",
        "Cola de emails pendientes creciendo",
        "Dirección de email sospechosa detectada",
        "Límite diario de envíos próximo a alcanzarse"
    ],
    "ERROR": [
        "Email rechazado por destinatario - Buzón lleno",
        "Dirección de email inválida proporcionada",
        "Fallo al adjuntar archivo al email"
    ],
    "DEBUG": [
        "Validando formato de dirección de email",
        "Conectando con servidor SMTP en puerto 587",
        "Procesando plantilla de email",
        "Verificando lista de destinatarios",
        "Comprimiendo imágenes adjuntas"
    ]
}

# =====================================
# FUNCIÓN PARA GENERAR UN LOG ALEATORIO
# =====================================

# Esta funcion genera un log aleatorio del servicio de email
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

# ======================================
# FUNCIÓN PARA UN ENVIAR LOG AL SERVIDOR
# ======================================

# Esta funcion envía un log al servidor central
def enviar_log(log):
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

# =======================================
# BUCLE PRINCIPAL QUE GENERA Y ENVIA LOGS
# =======================================

# Bucle principal que genera y envía logs
def ejecutar_servicio():
    
    print("=" * 70)
    print(f"{NOMBRE_SERVICIO} INICIADO")
    print("=" * 70)
    print(f"Servidor destino: {URL_SERVIDOR}")
    print(f"Token: {TOKEN[:25]}...")
    print(f"Intervalo: {INTERVALO_MIN}-{INTERVALO_MAX} segundos")
    print(f"Presiona Ctrl+C para detener")
    print("=" * 70 + "\n")
    
    contador = 0
    
    try:
        while True:
            contador += 1
            
            log = generar_log()
            
            print(f"\n Enviando log #{contador}")
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