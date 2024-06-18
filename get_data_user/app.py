import json
import sys
import os
import logging

# Añade el directorio connection_db al sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'connection_db'))

# Importa las funciones necesarias desde connection_db
from connection_db.connection_db import connect_db, execute_query, close_connection

logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    rds_host = os.environ['RDS_HOST']
    rds_user = os.environ['DB_USERNAME']
    rds_password = os.environ['DB_PASSWORD']
    rds_db = os.environ['DB_NAME']

    query = f"SELECT * FROM users;"

    connection = connect_db(rds_host, rds_user, rds_password, rds_db)

    users = []

    if connection:
        try:
            results = execute_query(connection, query)
            close_connection(connection)
            if results:
                logging.info("Results:")
                for row in results:
                    user = {
                        'id_usr': row[0],
                        'name_usr': row[1],
                        'lastname_usr': row[2],
                        'email_usr': row[3],
                        'phone_usr': row[4]
                    }
                    users.append(user)
                    logging.info(row)
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "Get Users",
                        "data": users
                    })
                }
            else:
                return {
                    "statusCode": 204,
                    "body": json.dumps({"message": "No results found."})
                }
        except Exception as e:
            logging.error("Error executing query: %s", e)
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "An error occurred while processing the request."})
            }
    else:
        logging.error("Connection to the database failed.")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to connect to the database."})
        }
