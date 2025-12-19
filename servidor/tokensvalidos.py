"""
Sistema de autenticacion con tokens 
Cada servicio tiene su propio token unico para enviar logs.
"""

# Definimos un diccionario con tokens validos donde la clave es el token y el valor es el nombre del servicio, esto lo hacemos para validar un token y saber a que servico pertenece.
TOKENS_VALIDOS = {
    "Token AUTH_SERVICE_2024": "AuthService",
    "Token PAYMENT_SERVICE_2024": "PaymentService",
    "Token EMAIL_SERVICE_2024": "EmailService",
    "Token ADMIN_2024": "AdminService"
}

#==============
# VALIDAR TOKEN
#==============

# Definimos una funcion para validar tokens
def validar_token(token):

    if not token:
        return None # devolvemos none porque en este caso buscamos algo, no resppondemos a una pregunta.
    
    # Verificamos si el token recibido comienza exactamente igual con la palabra Token y es espacio.
    if not token.startswith("Token "):
        return None
    
    # Buscamos el token recibido en el diccionario de tokens validos que definimos. Si lo encontramos devuelve el nombre del servicio y si no, devuelve none y lo rechaza.
    servicio = TOKENS_VALIDOS.get(token)

    return servicio

# =======================================
# OBTENER TODOS LOS SERVICIOS REGISTRADOS
# =======================================

# Esta funcion devuelve una lista de servicios que tienen tokens validos.
def obtener_servicios():

    # devolvemos una lista con los valores del diccionario que son los nombres de los servicios.
    return list(TOKENS_VALIDOS.values())

