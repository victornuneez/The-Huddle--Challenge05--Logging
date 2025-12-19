"""
SERVIDOR CENTRAL DE LOGGING DISTRIBUIDO(LUGAR DONDE SE JUNTAN TODOS LOS REGISTROS(LOGS)).

FUNCIONALIDADES:
1- Recibe logs de otros servicios.
2- Verifica que esten autorizados.
2- Guarda los logs en base de datos.
3- Consulta logs por GET/logs (con filtros opcionales).
"""

# Se importa del modulo flask la clase Flask, sirve para crear y gestionar el servidor.
from flask import Flask

# Importamos del modulo flask, "el objeto request" que permite al servidor acceder a todos los datos de las peticiones HTTP que envien los servicios o clientes.
from flask import request

# Importamos la funcion jsonify que sirve para devolver respuestas json que los servicios puedan entender facilmente.(El programa habla siempre en json)
from flask import jsonify

from basededatos import guardar_log, guardar_logs_multiples, obtener_logs
from tokensvalidos import validar_token, obtener_servicios

#=============================
# INICIALIZAR APLICACION FLASK
#=============================
# Creamos y preparamos el servidor web (objeto) Flask, con 'name' le decimos que desde aca comienza el archivo principal y aca esta todos los recursos que necesita.
app = Flask(__name__)


#=============================
# ENDPOINT 1: PAGINA DE INICIO 
#=============================

# Decorador de Flask que conecta la URL raiz(/ = pagina principal) con la funcion inicio. 
@app.route('/')

# Esta funcion devuelve informacion del servidor. Se devuelve un JSON valido y el codigo 200 en forma de tupla para que flask lo convierta en una respuesta HTTP. 
def inicio():
    return jsonify({
        "nombre": "Servidor de Logging Distruibuido",
        "version": "1.0",
        "estado": "activo",
    
    # lista de rutas que tiene el servidor y como se usan.
        "endpoints": {
            "raiz": "GET /",
            "recibir_logs": "POST /logs (requiere autenticacion)",
            "consultar_logs": "GET /logs (filtros opcionales)"
        },
        
        # Mostramos todos los servicios que estan enviando logs al servidor con la funcion 'obtener_servicios'.
        "servicios_registrados": obtener_servicios()
    }), 200


#======================================
# ENDPOINT 2: RECIBIR LOGS (POST /logs)
#======================================

# Este decorador flask asocia la URL "/logs" a la funcion 'recibir_logs' que solo acepta solicitudes POST.
@app.route('/logs', methods=['POST'])

# Esta funcion recibe registros de logs(eventos) de diferentes servicios y los guarda en la base de datos.
def recibir_logs():

# --------------
# VALIDAR TOKENS
# --------------
    # Miramos si la peticion HTTP tiene un token de autorizacion en su header y lo guardamos para poder usarlo.
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({
            "Error": "Falta el header Authorization"
        }), 401 # Error 401 significa: No autorizado.
    
    # Devuelve el nombre del servicio en caso de que el token sea valido. Determinamos quien envia el log y si es valido.
    servicio_autorizado = validar_token(token)

    if not servicio_autorizado:
        return jsonify({
            "Error": "Token invalido o no autorizado"
        }), 403 # Tiene un token pero su token es invalido(no tiene permiso).
    
    # Se imprime un mensaje en pantalla para ver el token valido y que servicio esta conectado. 
    print(f"Servicio autenticado: {servicio_autorizado}")

# -------------
# RECIBIR DATOS
#--------------
    # Agarramos el cuerpo(body) de la peticion y lo convertimos y guardamos en un diccionario de python.
    datos = request.get_json()

    # filtro para no intentar procesar un log vacio.
    if not datos: 
        return jsonify({
            "Error": "No se enviaron datos en el body"
        }), 400 # Error 401: significa que la peticion esta mal armada, falta algo que debia venir(body)
    

#---------------------------------------------------------------------
# PROCESAR LOGS DE MANERA DISTINTA SEGUN SEA UN SOLO LOG O VARIOS LOGS
#---------------------------------------------------------------------

#----------------------------------------------
# CASO 1: SE RECIBIO UN SOLO LOG (DICCIONARIO)
#----------------------------------------------
    
    # Condicional que verifica que datos sea un diccionario, si es un diccionario significa que datos contiene un solo log. 
    if isinstance(datos, dict):
        # Lista con los nombres de los campos obligatorios que los servicios o clientes deben enviar en el body.
        campos_requeridos = ['timestamp', 'service', 'severity', 'message']

        # Este bucle recorre la lista uno por uno y revisa si cada campo esta en el diccionario datos.(Si falta alguno devuelve un JSON con el error)
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({
                    "Error": f"Falta el campo requerido: {campo}"
                }), 400

        # El log recibido paso las validaciones y tiene los campos correctos entonces procedemos a guardar todos sus campos en la base de datos.
        exito = guardar_log(
            timestamp=datos['timestamp'],
            service=datos['service'],
            severity=datos['severity'],
            message=datos['message']
        )

        # Verificamos si el log se guardo bien en la base de datos, si se guardo bien devolvemos un mensaje indicando que todo salio bien.
        if exito:
            return jsonify({
                "status": "success",
                "mensaje": "Log guardado correctamente",
                "servicio": servicio_autorizado
            }), 201 # Codigo 201 significa: que se creo un recurso nuevo.
        
        # Si exito devolvio false, significa que el log no se pudo guardar correctamente por algun error interno del servidor.
        else:
            return jsonify({
                "Error": "Error al guardar el log en la base de datos"
            }), 500 # Codigo 500 significa: Error interno del servidor, el error es del servidor.
    
    #---------------------------------------------
    # CASO 2: SE RECIBIERON MULTIPLES LOGS (LISTA)
    #---------------------------------------------
    # Se verifica si datos es una lista, si es una lista entonces contiene una lista de diccionario de logs.
    elif isinstance(datos, list):
        # Lista con los campos obligatorios que deben tener los body de los logs que se recibieron.
        campos_requeridos = ['timestamp', 'service', 'severity', 'message']

        # Recorremos cada log que vino en la lista 'datos'. "i" es el numero de log y 'log' el contenido de cada log
        for i, log in enumerate(datos):

            # Se recorre cada campo obligatorio y se verifica que cada log tenga cada campo requerido, si no tienen se devuelve un mensaje indicando que log no tiene un campo re.
            for campo in campos_requeridos:
                if campo not in log:
                    return jsonify({
                        "Error": f"Log #{i+1}: Falta el campo {campo}"
                    }), 400 # Codigo 400: Falta algo que debia venir.

        # Guarda todos los logs en la base de datos una vez validados. Y devuelve cuantos logs se guardaron correctamente.
        cantidad_guardada = guardar_logs_multiples(datos)

        # Devolvemos una respuesta HTTP en formato json al servicio que hizo la peticion, contando cuantos logs se guardaron, quien los envio y cuantos llegaron.
        return jsonify({
            "status": "success",
            "mensaje": f"{cantidad_guardada} logs guardados correctamente",
            "servicio": servicio_autorizado,
            "total_recibido": len(datos)
        }),201 # Codigo 201 significa: Created se creo un recurso nuevo.

    else:
        return jsonify({
            "Error": "Formato invalido. Envia un objeto JSON o un array de objetos"
        }), 400 # Codigo 400: Falta algo que debia venir.
    

#=======================================
# ENDPOINT 3: CONSULTAR LOGS (GET /logs)
#=======================================

# Este decorador flask asocia la ruta /logs a la funcion consultar logs, pero esta funcion solo se ejecuta si llegan peticiones HTTP por el metodo GET.
@app.route('/logs', methods=['GET'])
def consultar_logs():
    """
    EJ: De como un servicio envia una peticion con parametros.
        GET /logs?timestamp_start=2025-11-29%2000:00:00 
    """

    # Este bloque se ejecuta cuando un cliente o servicio hace una consulta con filtros de los logs guardados en el servidor. 
    # estas variables toman el valor del filtro que se solicita.
    timestamp_start = request.args.get('timestamp_start')
    timestamp_end = request.args.get('timestamp_end')
    received_at_start = request.args.get('received_at_start')
    received_at_end = request.args.get('received_at_end')

    logs = obtener_logs(
        timestamp_start = timestamp_start,
        timestamp_end = timestamp_end,
        received_at_start = received_at_start,
        received_at_end = received_at_end
    )

    # Se devuelve la respuesta a la peticion con filtros que realizo el cliente o servicio en formato JSON.
    return jsonify({
        "status": "success",
        "total": len(logs), # intdica cuantos logs encontro y va a devolver.
        "filtros_aplicados": { # muestra que filtros se aplicaron
        "timestamp_start": timestamp_start,
        "timestamp_end": timestamp_end,
        "received_at_start": received_at_start,
        "received_at_end": received_at_end
        },
        "logs": logs # contiene la lista real de logs que cumplen con los filtros.
    }), 200 # Codigo 200 significa: que todo salio bien HTTP de exito.

# Este bloque se ejecuta solo si corremos este archivo directamente,
# evita que cuando alguin importa el archivo y solo quiera usar una funcion, se ejecute todo el codigo del servidor.
if __name__ =='__main__':
    print("SERVIDOR DE LOGGING DISTRIBUIDO\n")
    print("URL: http//localhost:5000")
    print("\nENDPOINTS DISPONIBLES:")
    print("GET  /     -> Información del servidor")
    print("POST /logs -> Recibir logs (requieren un token de autorizacion)")
    print("GET  /logs -> Consultar logs (filtros opcionales)")
    print("\nTOKENS VÁLIDOS:")
    print("   - Token AUTH_SERVICE_2024    -> AuthService")
    print("   - Token PAYMENT_SERVICE_2024 -> PaymentService")
    print("   - Token EMAIL_SERVICE_2024   -> EmailService")

# Arrancamos el servidor,(host='0.0.0.0') permite que el servidor acepte conexiones de cualquier IP.
# En el puerto 5000 el servidor esta escuchando las peticiones. 
# (debug=True) muestra errores y recarga cambios automaticamente.
app.run(debug=True, port=5000, host='0.0.0.0')