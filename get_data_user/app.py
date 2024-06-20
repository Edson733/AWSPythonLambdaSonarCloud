import json
import os
import logging

# Importa las funciones necesarias desde connection_db
from get_data_user.connection_db import connect_db, execute_query, close_connection

# Configura el nivel de logging a INFO
logging.basicConfig(level=logging.INFO)


# Definición de la función lambda_handler, la cual es el punto de entrada para la ejecución Lambda
def lambda_handler(event, context):
    # Obtiene las variables de entorno necesarias para la conexión a la base de datos
    rds_host = os.environ['RDS_HOST']
    rds_user = os.environ['DB_USERNAME']
    rds_password = os.environ['DB_PASSWORD']
    rds_db = os.environ['DB_NAME']

    # Define la consulta SQL que se ejecutará
    query = f"SELECT * FROM users;"

    # Establece la conexión a la base de datos usando las credenciales y parámetros obtenidos
    connection = connect_db(rds_host, rds_user, rds_password, rds_db)

    # Inicializa una lista vacía para almacenar los usuarios
    users = []

    # Verifica si la conexión fue exitosa
    if connection:
        try:
            # Ejecuta la consulta SQL
            results = execute_query(connection, query)
            # Verifica si se obtuvieron resultados
            if results:
                logging.info("Results:")
                # Itera sobre cada fila de resultados y los almacena en el diccionario `user`
                for row in results:
                    user = {
                        'id_usr': row[0],
                        'name_usr': row[1],
                        'lastname_usr': row[2],
                        'email_usr': row[3],
                        'phone_usr': row[4]
                    }
                    # Añade el diccionario `user` a la lista `users`
                    users.append(user)
                    # Loggea cada fila obtenida
                    logging.info(row)
                # Retorna un diccionario con el código de estado 200 y los datos de los usuarios en formato JSON
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "Get Users",
                        "data": users
                    })
                }
            else:
                # Retorna un diccionario con el código de estado 204 si no se encontraron resultados
                return {
                    "statusCode": 204,
                    "body": json.dumps({"message": "No results found."})
                }
        except Exception as e:
            # Captura y loggea cualquier excepción ocurrida durante la ejecución de la consulta
            logging.error("Error executing query: %s", e)
            # Retorna un diccionario con el código de estado 500 y un mensaje de error
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "An error occurred while processing the request."})
            }
        finally:
            # Cierra la conexión a la base de datos
            close_connection(connection)
    else:
        # Loggea un error si la conexión a la base de datos falló
        logging.error("Connection to the database failed.")
        # Retorna un diccionario con el código de estado 500 y un mensaje de error
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to connect to the database."})
        }
