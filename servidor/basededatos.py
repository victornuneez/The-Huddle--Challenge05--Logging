"""
Usamos la base de datos sqlite3 para guardar los logs que se reciban. Y necesitamos saber la hora en que llegan.
Sin esto el sistema seria ciego y olvidadiso.
"""

# Es un modulo que nos permite crear o conectarnos a una base de datos existente.Tambien nos permite comunicarnos con la base de datos.
import sqlite3

# Se importa del modulo 'datetime' la clase datetime que sirve para saber la fecha y la hora actual del sistema.
from datetime import datetime

# Guardamos el nombre de la base de datos en una variable. Por convencion una variable cuando esta en mayusculas se considera una constante.
NOMBRE_BD = "logs.db"

# ==============================
# CREAR LA BASE DATOS Y LA TABLA
# ==============================

""" 
Esta funcion se encarga de crear la tabla logs si no existe y si ya existe se conecta a la base de datos, esto evita errores cuando se arranca el servidor.
"""
def inicializar_base_datos():

    # Si el archivo logs no existe lo crea, y si existe se conecta y lo abre.
    conexion = sqlite3.connect(NOMBRE_BD)

    # El cursor es como el interprete que nos permite comunicarnos con la base de datos. Sin el cursor no se puede ejecutar comandos SQL.
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            received_at TEXT NOT NULL,
            service TEXT NOT NULL,
            severity TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')

    # Guarda los cambios realizados y se cierra la conexion para no dejar recursos abiertos.
    conexion.commit()
    conexion.close()
    print("Base de datos inicializada correctamente")

# ====================================
# GUARDAR UN LOG EN LA BASE DE DATOS
# ====================================

"""
Esta funcion sirve para recibir los datos de un log y guardarlos en la base de datos, sin esta funcion no se guardarian los datos de un log en ningun lado.
"""
def guardar_log(timestamp, service, severity, message):

    try:
        conexion = sqlite3.connect(NOMBRE_BD)
        cursor = conexion.cursor()
        
        # guardamos el momento cuando nuestro servidor recibe el log.
        received_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Inserta una fila nueva en la tabla Logs, inserta un log con sus datos a la tabla Logs.
        cursor.execute('''
            INSERT INTO Logs (timestamp, received_at, service, severity, message)
            VALUES (?,?,?,?,?)
        ''', (timestamp, received_at, service, severity, message))
        
        # Guarda los cambios realizados y liberamos recursos.
        conexion.commit()
        conexion.close()

        # Mostramos un resumen del log que se acaba de guardar para tener una vista previa
        # Retorna True si guardo el log correctamente en la tabla de la base de datos.
        print(f"Log guardado: {service} = {severity} - {message[:50]}")
        return True 
    
    # Tomamos cualquier error que pudo suceder y lo mostramos en pantalla.
    except Exception as error:
        print(f"Error al guardar el log: {error}")
        return False
    
# ======================
# GUARDAR MULTIPLES LOGS
# ======================

"""
Esta funcion guarda varios o multiples logs todos de una sola vez. Abre la base de datos inserta todo de una vez y cierra la base de datos.
"""
def guardar_logs_multiples(lista_logs):

    # Inicializamos un contador, esto sirve para saber cuantos logs se guardaron en la base de datos.
    contador = 0

    # Todos los logs comparten este 'received_at' porque todos llegan juntos al mismo tiempo. Se guarda la hora, fecha en que el servidor los recibio.
    received_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conexion = sqlite3.connect(NOMBRE_BD)
        cursor = conexion.cursor()

        # Obtenemos cada log de la lista_logs e insertamos sus datos en la base de datos. 
        for log in lista_logs:
            cursor.execute('''
                INSERT INTO Logs (timestamp, received_at, service, severity, message)
                VALUES (?,?,?,?,?)
            ''', (
                log.get('timestamp'), # Usamos la funcion 'get' para obtener el dato correspondiente a cada columna sin romper el flujo si un campo esta vacio.
                received_at,
                log.get('service'),
                log.get('severity'),
                log.get('message')
            ))
            # Cada log insertado suma
            contador += 1

        # Una vez insertado cada log en la base de datos, guardamos los cambios y cerramos la conexion con la base de datos.
        conexion.commit()
        conexion.close()

        print(f"{contador} logs guardados correctamente")
        return contador # Devuelve cuantos logs se guardaron correctamente en la base de datos.
    
    except Exception as error:
        print(f"Error al guardar logs: {error}")
        return contador # Devolvemos cuantos logs se pudieron guardar antes de que surja el problema.

#============================
# OBTENER LOGS USANDO FILTROS
#============================ 

"""
Esta funcion sirve para obtener los logs de la base de datos segun filtros de hora en que el servicio creo el log y la hora en el que el servidor recibio el log
"""
def obtener_logs(timestamp_start=None, timestamp_end=None, 
                received_at_start=None, received_at_end=None):
    try:
        conexion = sqlite3.connect(NOMBRE_BD)
        conexion.row_factory = sqlite3.Row # Con esta linea cambiamos la tupla que nos devuelve 'SELECT' a un objeto que se comporta como un diccionario.(Une Columna -> Valor)
        cursor = conexion.cursor()

        # Con WHERE 1=1 indicando que la condicional es siempre True no filtra nada, esto nos permite agregar mas condicionales para filtrar los datos que necesitamos.
        consulta = "SELECT * FROM Logs WHERE 1=1"
        parametros = [] # aca se guardara los valores que reemplazaran los ? en la consulta.

        if timestamp_start:
            consulta += " AND timestamp >= ?"
            parametros.append(timestamp_start) 

        if timestamp_end:
            consulta += " AND timestamp <= ?"
            parametros.append(timestamp_end) 

        if received_at_start:
            consulta += " AND received_at >= ?"
            parametros.append(received_at_start)

        if received_at_end:
            consulta += " AND received_at <= ?"
            parametros.append(received_at_end)

        # Ordena de forma descendiente, los logs mas recientes aparecen primero.
        consulta += " ORDER BY received_at DESC"

        # Ejecuta las consultas SQL reeplazando los ? con los filtros que pusimos en los parametros segun su orden.(Este proceso se hace en la base de datos al ejecutar la consulta)
        cursor.execute(consulta, parametros)

        # Con fetchall() se trae todos los logs que cumplieron los filtros y las guarda en la variable 'resultados'.
        resultados = cursor.fetchall()

    # Lista de diccionarios donde se guardan los logs.(Estructura de datos universal que cualquier programa puede leer y utlizar)
        logs = []

    # Este bucle recorre cada fila que devolvio sqlite y convierte los resultados en una lista de diccionarios de Python. (Mas facil de usar)
        for fila in resultados:
            logs.append({           # Crea una etiqueta llamada 'id' y le asígna el valor que encuentra en la columna 'id' de la base de datos.(Asi sucesivamente)
                "id": fila["id"],
                "timestamp": fila["timestamp"],
                "received_at": fila["received_at"],
                "service": fila["service"],
                "severity": fila["severity"],
                "message":fila["message"]
            })
        
        conexion.close()
        print(f"Se encontraron {len(logs)} logs")   # Mostramos en pantalla cuantos logs se obtuvieron de la base de datos.
        return logs                                 # Devuelve la lista de diccionarios con los logs filtrados a quien haya llamado la funcion.
                                                    # Esto permite trabajar con estos datos en otras partes del programa.
    

    # Capturamos cualquier error que haya ocurrido.
    except Exception as error:
        print(f"Error al obtener logs: {error}")
        return [] # Devuelve una lista vacia para que el codigo que llamo la funcion siga funcionando sin problemas, sin romperse.


# inicializamos la base de datos para que todo lo demas funcione sin problemas. nos aseguramos que la tabla logs exista antes de intentar guardarr o consultar registros.
# evitamos errores como no existe la tabla logs.
inicializar_base_datos()


