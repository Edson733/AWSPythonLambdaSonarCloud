import json
import pymysql
import os

rds_host = os.environ['RDS_HOST']
rds_user = os.environ['DB_USERNAME']
rds_password = os.environ['DB_PASSWORD']
rds_db = os.environ['DB_NAME']

def lambda_handler(event, context):
    connection = pymysql.connect(
        host=rds_host,
        user=rds_user,
        password=rds_password,
        database=rds_db
    )

    users = []

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            result = cursor.fetchall()

            for row in result:
                user = {
                    'id_usr': row[0],
                    'name_usr': row[1],
                    'lastname_usr': row[2],
                    'email_usr': row[3],
                    'phone_usr': row[4]
                }
                users.append(user)
    finally:
        connection.close()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Get Users",
            "data": users
        }),
    }
