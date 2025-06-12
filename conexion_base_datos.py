# conexion_base_datos.py
# Módulo para operaciones básicas con MySQL usando PyMySQL
# En caso de no tener instalado pymysql, instalar con:
# pip install pymysql

import pymysql
from config import get_mysql_config

def get_connection():
    """
    Crea y devuelve una conexión a la base de datos MySQL.
    """
    cfg = get_mysql_config()
    return pymysql.connect(
        host=cfg['host'],
        port=cfg['port'],
        user=cfg['user'],
        password=cfg['password'],
        database=cfg['database'],
        charset=cfg['charset']
    )

def execute_query(sql, params=None, fetch=False):
    """
    Ejecuta una sentencia SQL.
    - sql: texto de la consulta o comando.
    - params: tupla de parámetros para placeholders (%s).
    - fetch: si es True, devuelve cursor.fetchall().
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            if fetch:
                return cur.fetchall()
            conn.commit()
    finally:
        conn.close()

# Ejemplos de uso:
if __name__ == "__main__":
    # 1) Crear tablas (leer de scripts_integrador2.sql)
    # execute_query(open('scripts_integrador2.sql').read())

    # 2) Insertar datos de ejemplo
    # execute_query("INSERT INTO clientes (id, nombre, email) VALUES (%s,%s,%s)", (1,'Ana','ana@ej.com'))

    # 3) Consultar
    # rows = execute_query("SELECT * FROM clientes", fetch=True)
    # for row in rows:
    #     print(row)
    pass
