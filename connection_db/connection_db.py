import pymysql  # Importa el módulo pymysql, que se utiliza para interactuar con bases de datos MySQL.
import logging  # Importa el módulo logging para registrar mensajes de log.

# Configura el sistema de logging para que registre mensajes a partir del nivel INFO.
logging.basicConfig(level=logging.INFO)


def connect_db(host, user, password, database):  # Función para establecer una conexión con la base de datos.
    try:
        # Intenta establecer una conexión con la base de datos utilizando los parámetros proporcionados.
        connection = pymysql.connect(
            host=host,  # Dirección del servidor de la base de datos.
            user=user,  # Nombre de usuario para la autenticación.
            password=password,  # Contraseña para la autenticación.
            database=database  # Nombre de la base de datos a la que se quiere conectar.
        )
        # Si la conexión es exitosa, registra un mensaje de información.
        logging.info("Connection established successfully.")
        return connection  # Devuelve el objeto de conexión.
    except Exception as e:
        # Si ocurre un error, registra un mensaje de error con la descripción del problema.
        logging.error("Error connecting to the database: %s", e)
        return None  # Devuelve None si la conexión falla.


def execute_query(connection, query):  # Función para ejecutar una consulta SQL en la base de datos.
    try:
        # Utiliza un cursor para interactuar con la base de datos.
        with connection.cursor() as cursor:
            cursor.execute(query)  # Ejecuta la consulta SQL proporcionada.
            result = cursor.fetchall()  # Recupera todos los resultados de la consulta.
            return result  # Devuelve los resultados de la consulta.
    except Exception as e:
        # Si ocurre un error al ejecutar la consulta, registra un mensaje de error con la descripción del problema.
        logging.error("Error executing query: %s", e)
        return None  # Devuelve None si la ejecución de la consulta falla.


def close_connection(connection):  # Función para cerrar la conexión con la base de datos.
    if connection:  # Verifica si el objeto de conexión es válido (no es None).
        connection.close()  # Cierra la conexión.
        # Registra un mensaje de información indicando que la conexión se cerró correctamente.
        logging.info("Connection closed successfully.")
