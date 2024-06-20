import json
import os
import unittest
from unittest.mock import patch
from get_data_user import app


# Define una clase para pruebas unitarias de la aplicación
class TestApp(unittest.TestCase):

    # Prueba para una ejecución exitosa del manejador lambda con resultados
    @patch.dict(os.environ, {
        'RDS_HOST': 'test_host',  # Imita la variable de entorno para el host de la BD
        'DB_USERNAME': 'test_user',  # Imita la variable de entorno para el usuario de la BD
        'DB_PASSWORD': 'test_password',  # Imita la variable de entorno para la contraseña de la BD
        'DB_NAME': 'test_db'  # Imita la variable de entorno para el nombre de la BD
    })
    @patch('get_data_user.app.connect_db')  # Imita la función connect_db
    @patch('get_data_user.app.execute_query')  # Imita la función execute_query
    @patch('get_data_user.app.close_connection')  # Imita la función close_connection
    def test_lambda_handler_success(self, mock_close_connection, mock_execute_query, mock_connect_db):
        # Simula una conexión exitosa y resultados de consulta
        mock_connect_db.return_value = True  # Imita connect_db para devolver True indicando una conexión exitosa
        mock_execute_query.return_value = [  # Imita execute_query para devolver datos de usuario de ejemplo
            {
                "id_usr": 1,
                "name_usr": 'John',
                "lastname_usr": 'Doe',
                "email_usr": 'john.doe@example.com',
                "phone_usr": '1234567890'
            }
        ]
        event = {}  # Define un evento simulado para el manejador lambda
        context = None  # Define un contexto simulado para el manejador lambda
        result = app.lambda_handler(event, context)  # Llama al manejador lambda
        self.assertEqual(result['statusCode'], 200)  # Verifica que el código de estado sea 200 (OK)
        body = json.loads(result['body'])  # Analiza el cuerpo de la respuesta
        self.assertEqual(body['message'], 'Get Users')  # Verifica que el mensaje en la respuesta sea 'Get Users'
        self.assertTrue('data' in body)  # Verifica que la respuesta contenga 'data'
        self.assertEqual(len(body['data']), 1)  # Verifica que 'data' contenga exactamente un usuario
        mock_close_connection.assert_called_once_with(True)  # Verifica que close_connection sea llamado con True

    # Prueba para una ejecución exitosa del manejador lambda sin resultados
    @patch.dict(os.environ, {
        'RDS_HOST': 'test_host',
        'DB_USERNAME': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_NAME': 'test_db'
    })
    @patch('get_data_user.app.connect_db')
    @patch('get_data_user.app.execute_query')
    @patch('get_data_user.app.close_connection')
    def test_lambda_handler_no_results(self, mock_close_connection, mock_execute_query, mock_connect_db):
        # Simula una conexión exitosa pero sin resultados de consulta
        mock_connect_db.return_value = True
        mock_execute_query.return_value = []  # Imita execute_query para devolver una lista vacía
        event = {}
        context = None
        result = app.lambda_handler(event, context)
        self.assertEqual(result['statusCode'], 204)  # Verifica que el código de estado sea 204 (Sin Contenido)
        body = json.loads(result['body'])
        # Verifica el mensaje en la respuesta sea 'No results found.'
        self.assertEqual(body['message'], 'No results found.')
        mock_close_connection.assert_called_once_with(True)

    # Prueba para una ejecución del manejador lambda con un error en la consulta
    @patch.dict(os.environ, {
        'RDS_HOST': 'test_host',
        'DB_USERNAME': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_NAME': 'test_db'
    })
    @patch('get_data_user.app.connect_db')
    @patch('get_data_user.app.execute_query')
    @patch('get_data_user.app.close_connection')
    def test_lambda_handler_query_error(self, mock_close_connection, mock_execute_query, mock_connect_db):
        # Simula una conexión exitosa pero un error en la ejecución de la consulta
        mock_connect_db.return_value = True
        # Imita execute_query para lanzar una excepción
        mock_execute_query.side_effect = Exception('Query execution error')
        event = {}
        context = None
        result = app.lambda_handler(event, context)
        # Verifica que el código de estado sea 500 (Error Interno del Servidor)
        self.assertEqual(result['statusCode'], 500)
        body = json.loads(result['body'])
        # Verifica que el error en la respuesta sea 'An error occurred while processing the request.'
        self.assertEqual(body['error'], 'An error occurred while processing the request.')
        mock_close_connection.assert_called_once_with(True)

    # Prueba para una ejecución del manejador lambda con un fallo en la conexión a la BD
    @patch.dict(os.environ, {
        'RDS_HOST': 'test_host',
        'DB_USERNAME': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_NAME': 'test_db'
    })
    @patch('get_data_user.app.connect_db')
    def test_lambda_handler_connection_fail(self, mock_connect_db):
        # Simula un fallo en la conexión a la base de datos
        mock_connect_db.return_value = None  # Imita connect_db para devolver None indicando un fallo en la conexión
        event = {}
        context = None
        result = app.lambda_handler(event, context)
        self.assertEqual(result['statusCode'], 500)
        body = json.loads(result['body'])
        # Verifica que el error en la respuesta sea 'Failed to connect to the database.'
        self.assertEqual(body['error'], 'Failed to connect to the database.')
        # Verifica que connect_db se haya llamado una vez con los parámetros correctos
        mock_connect_db.assert_called_once_with('test_host', 'test_user', 'test_password', 'test_db')
