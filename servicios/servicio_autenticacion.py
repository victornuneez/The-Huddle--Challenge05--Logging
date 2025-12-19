"""
Este es un servicio simulado de autenticacion que genera logs y los envia al servidor central.

Simula estos eventos:
- Inicios de sesion exitosos
- Intentos de login fallidos
- Tokens invalidos
- Verificaciones de login correctos
"""

# Este modulo sirve para hacer peticiones HTTP, lo usamos para enviar logs al servidor(app.py)
import requests

# Con el modulo random podemos enviar logs aleatorios al servidor para simular cualquier caso que pueda ocurrir en la vida real.
import random

# Importamos del modulo datetime la clase datetime, sirve para trabajar con fechas y horas para saber cuando paso algo, guardarlas y compararlas.
from datetime import datetime

# Importamos el modulo time para hacer pausas entre logs, para enviar logs con un tiempo de diferencia para simular usuarios reales, actividad continua.
import time 

# ======================================
# VALORES Y CONFIGURACIONES DEL SERVICIO
# ======================================

# Definimos el nombre del servicio para que el servicio se identifique y el servidor sepa que servicio le envia un log.
NOMBRE_SERVICIO = "AuthService"

# Definimos un token valido, que autoriza a nuestro servicio simulado ingresar al servidor.(tiene que ser un token valido del servidor)
TOKEN = "Token AUTH_SERVICE_2024"

# Definimos la URL a donde el servicio debe enviar sus logs y con que funcion especifica del servidor debe comunicarse(ENDPOINT:"/logs").
URL_SERVIDOR = "http://localhost:5000/logs"

# Definimos dos intervalos en donde con las funciones de random se enviaran logs con esos intervalos de manera aleatoria.
INTERVALO_MIN = 2
INTERVALO_MAX = 4


# ================================================
# NIVELES DE SEVERIDADES CON SUS POSIBLES MENSAJES
# ================================================

"""
INFO = algo normal
WARNING = algo raro paso pero sigue andando
ERROR = algo fallo
DEBUG = informacion tecnica
"""

# Definimos una lista de severidades posibles de un log.(Eventos)
niveles = ["INFO", "WARNING", "ERROR", "DEBUG"]

# Definimos en un diccionario que tipo de mensajes y con que nivel de gravedad enviar al servidor.(clave = nivel de severidad, valor = lista de mensajes posibles para ese nivel).
mensajes_por_nivel = {
    "INFO": [
        "Usuario inicio sesion correctamente",
        "Sesion cerrada por el usuario",
        "Token de acceso renovado exitosamente",
        "Verificacion de credenciales exitosa",
        "Nuevo usuario registrado en el sistema"
    ],
    "WARNING": [
        "Intento de login con usuario inexistente",
        "Contrasenha incorrecta",
        "Sesion expirada, requiere re-autenticacion",
        "IP sospechosa detectada en intento de login",
        "Usuario bloqueado temporalmente por multiples intentos fallidos"
    ],
    "ERROR": [
        "Token invalido recibido en la peticion",
        "Error al verificar credenciales en base de datos",
        "Servicio de autenticacion no responde",
        "Fallo al generar token de acceso",
        "Base de datos de usuarios no disponible"
    ],
    "DEBUG": [
        "Chequeando credenciales del usuario en BD",
        "Generando hash de contrasenha",
        "Validando formato de email proporcionado",
        "Verificando permisos de usuario",
        "Consultando cache de sesiones activas"
    ]
}

# ======================================
# FUNCION PARA GENERAR UN LOG ALEATORIO.
# ======================================

# Esta funcion genera un log aleatorio y retorna un Diccionario con los datos del log.
def generar_log():
    
    nivel = random.choice(niveles)
    mensaje = random.choice(mensajes_por_nivel[nivel]) # Toma la lista de mensajes del nivel de severidad seleccionado.

    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service": NOMBRE_SERVICIO,
        "severity": nivel,
        "message": mensaje
    }

    return log

# ======================================
# FUNCION PARA ENVIAR UN LOG AL SERVIDOR
# ======================================

# Esta funcion envia un log al servidor central, usa como argumento el log(diccionario con los datos del log).
def enviar_log(log):

    try:
        # Este header indica que los datos de este log estan en json y que contiene el token del servicio que le autoriza el acceso al servidor.
        headers = {
            "Content-Type": "application/json",
            "Authorization": TOKEN
        }
        
        # Enviamos el log al servidor en formato json, con los datos extra para el servidor(token/formato), ponemos un limite de espera de 5 segundos, la peticion falla pasados 5s.
        # La variable respuesta guarda todo lo que el servidor devuelva o responda.  
        respuesta = requests.post(URL_SERVIDOR, json=log, headers=headers, timeout=5)

        # Verificamos si el servidor acepto y guardo el log correctamente.
        if respuesta.status_code == 201:
            print(f"Log enviado: [{log['severity']}] {log['message'][:50]}") # "[:50] muestra los primeros 50 caracteres"
            return True # Termina la funcion indicando que todo salio bien.
        
        # Si hubo algun error al enviar el log al servidor, imprimimos en pantalla el codigo HTTP que devolvio el servidor y el mensaje de error.
        else: 
            print(f"Error {respuesta.status_code}: {respuesta.text}")
            return False # Termina la funcion indicando que el log fallo
        
    except Exception as error:
        print(f"Error inesperado: {error}")
        return False


# ================================================
# FUNCION PRINCIPAL: BUCLE QUE GENERA Y ENVIA LOGS
# ================================================

# Esta funcion genera y envia logs continuamente.
def ejecutar_servicio():
    
    print("=" * 70)
    print(f"{NOMBRE_SERVICIO} INICIADO")
    print("=" * 70)
    print(f"Servidor destino: {URL_SERVIDOR}")
    print(f"Token: {TOKEN}")
    print(f"Intervalo: {INTERVALO_MIN}-{INTERVALO_MAX} segundos")
    print("Presiona Ctrl+C para detener")
    print("=" * 70 + "\n")

    contador = 0

    # Bucle infinito para generar y enviar logs hasta que el usuario lo detenga.
    try:
        while True:
            contador += 1

            log = generar_log()

            print(f"Enviando log {contador}")
            enviar_log(log)
            print()

            # Generamos un numero aleatorio entre el min y el maximo, de espera para enviar el proximo log.
            espera = random.randint(INTERVALO_MIN, INTERVALO_MAX)
            print(f"Esperando {espera} segundos para envia el proximo log")
            time.sleep(espera)

    # Atrapa el error especial cuando el usuario detiene el programa desde el teclado(Ctrl+C). Sirve para detener limpiamente el programa.
    except KeyboardInterrupt:
        print(f"\n{"="*70}")
        print(f"{NOMBRE_SERVICIO} DETENIDO")
        print(f"Total de logs enviados: {contador}")
        print("=" * 70)

# Sirve para que solo se ejecute este script completo solo si se ejecuta directamente, evita que este servicio se ejecute automaticamente cuando es importado.
if __name__=="__main__":
    ejecutar_servicio()