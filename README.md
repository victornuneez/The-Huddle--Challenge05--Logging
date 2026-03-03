Sistema de Logging Distribuido (SLD)

Este proyecto es una solución robusta y modular para la centralización de registros (logs) procedentes de múltiples microservicios. Utiliza una arquitectura Cliente-Servidor sobre HTTP para recolectar, validar y almacenar eventos de sistema en tiempo real.

📁 Estructura del Proyecto

El proyecto se divide en dos grandes módulos:

/servidor: El núcleo que recibe, procesa y guarda la información.

- app.py: Servidor Flask y Endpoints.

- basededatos.py: Gestión de SQLite3.

- tokensvalidos.py: Sistema de seguridad y autenticación.

/servicios: Simuladores de microservicios independientes.

- auth_service.py: Gestión de sesiones y accesos.

- email_service.py: Notificaciones y eventos SMTP.

- payment_service.py: Transacciones y estados financieros.

🚀 Funcionalidades Principales

1. Servidor Central de Logging
Autenticación: Solo acepta logs de servicios con un Token de Autorización válido (Header Authorization).

Procesamiento Inteligente: Capacidad para recibir un solo log o una lista (batch) de múltiples logs en una sola petición.

Persistencia: Almacenamiento automático en base de datos SQLite con registro de received_at (marca de tiempo del servidor).

Consulta Avanzada: Endpoint GET con filtros por rango de fechas (tanto de origen como de recepción).

2. Microservicios (Simuladores)

Generación Aleatoria: Cada servicio simula eventos reales (INFO, WARNING, ERROR, CRITICAL) con mensajes específicos a su área.

Independencia: Cada servicio corre en su propio proceso y tiene su propio intervalo de envío.

Resiliencia: Manejo de errores y timeouts al intentar conectar con el servidor.

🛠️ Tecnologías Utilizadas

Python 3: Lenguaje principal.

Flask: Framework para el servidor web/API.

SQLite3: Base de datos relacional ligera.

Requests: Para la comunicación HTTP entre servicios.

JSON: Formato estándar para el intercambio de datos.

📊 Flujo de Datos

Un Servicio genera un evento (ej: "Pago rechazado").

Lo empaqueta en un JSON con su Token y lo envía vía POST a /logs.

El Servidor valida el token.

Si es válido, guarda el log en la Base de Datos.

Un administrador puede consultar los logs vía GET desde cualquier navegador o cliente API.

🚦 Cómo Ejecutar el Proyecto

Iniciar el Servidor:

Bash

cd servidor

python app.py

Iniciar los Servicios (en terminales separadas):

Bash

python servicios/auth_service.py

python servicios/email_service.py

python servicios/payment_service.py

🔍 Ejemplos de Consulta (API)

Para ver los logs guardados, puedes usar tu navegador o curl:

Ver todos: http://localhost:5000/logs

Filtrar por fecha: http://localhost:5000/logs?timestamp_start=2024-01-01 00:00:00

Nota: Este sistema está diseñado para ser escalable. Puedes añadir tantos servicios nuevos como quieras, simplemente registrando un nuevo token en tokensvalidos.py.
