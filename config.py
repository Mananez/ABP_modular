# config.py
# Configuración de conexión a la base de datos MySQL

import os

# Parámetros de conexión
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'tu_usuario')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'tu_contraseña')
MYSQL_DB = os.getenv('MYSQL_DB', 'skyroute')

def get_mysql_config():
    """
    Devuelve un diccionario con los parámetros de conexión a MySQL.
    """
    return {
        'host'     : MYSQL_HOST,
        'port'     : MYSQL_PORT,
        'user'     : MYSQL_USER,
        'password' : MYSQL_PASSWORD,
        'database' : MYSQL_DB,
        'charset'  : 'utf8mb4',
        'cursorclass': None  # usa el cursor por defecto
    }
