import mysql.connector
from mysql.connector import Error
from config import get_mysql_config

# Inicialización de la tabla 'clientes' si no existe
def init_db():
    """Crea la tabla clientes en MySQL si no existe."""
    cfg = get_mysql_config()
    conn = None # Inicializa conn fuera del try para asegurar que esté definida
    try:
        conn = mysql.connector.connect(**cfg)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id_Cliente INT AUTO_INCREMENT PRIMARY KEY,
                Nombre VARCHAR(20) NOT NULL,
                Apellido VARCHAR(20) NOT NULL,
                razon_social VARCHAR(150) NOT NULL,
                Documento_identidad VARCHAR(20) NOT NULL UNIQUE,
                Telefono INT, 
                correo VARCHAR(150) NOT NULL,
                fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
              DEFAULT CHARSET=utf8mb4
              COLLATE=utf8mb4_unicode_ci;
            """
        )
        conn.commit()
        print("Tabla 'clientes' verificada/creada correctamente.") # Mensaje de confirmación
    except Error as e:
        print(f"Error al inicializar la tabla clientes: {e}")
    finally:
        if conn and conn.is_connected(): # Verifica si conn fue creada y está conectada
            cursor.close()
            conn.close()


def agregar_cliente():
    """Permite agregar un cliente a la tabla 'clientes' en MySQL."""
    cfg = get_mysql_config()
    conn = None
    try:
        conn = mysql.connector.connect(**cfg)
        cursor = conn.cursor()
        print("\n--- AGREGAR CLIENTE ---")
        # Se solicita en el orden lógico para el usuario y para el SQL
        nombre              = input("Nombre: ").strip()
        apellido            = input("Apellido: ").strip()
        razon_social        = input("Razón social: ").strip()
        documento_identidad = input("DNI: ").strip()
        telefono            = input("Teléfono: ").strip() # Leer como string para validar o convertir
        correo              = input("Correo electrónico: ").strip()

        # Validar si el teléfono es un número antes de intentar convertirlo
        if not telefono.isdigit():
            print("Error: El teléfono debe contener solo dígitos.")
            return
        telefono = int(telefono) # Convertir a INT para la base de datos

        # Asegúrate de que el orden de las columnas coincida con el orden de las variables
        sql = """
            INSERT INTO clientes (Nombre, Apellido, razon_social, Documento_identidad, Telefono, correo) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, apellido, razon_social, documento_identidad, telefono, correo))
        conn.commit()
        print(f"Cliente '{razon_social}' agregado con DNI {documento_identidad}.")
    except Error as e:
        print(f"Error al agregar cliente: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def listar_clientes():
    """Muestra todos los clientes almacenados en la base de datos."""
    cfg = get_mysql_config()
    conn = None
    try:
        conn = mysql.connector.connect(**cfg)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Apellido, Nombre, razon_social, Documento_identidad, correo, Telefono FROM clientes")
        rows = cursor.fetchall()
        print("\n--- LISTADO DE CLIENTES ---")
        if not rows:
            print("No hay clientes registrados.")
            return
        for r in rows:
            print(f"Apellido: {r['Apellido']} | Nombre: {r['Nombre']} | Razón social: {r['razon_social']} | DNI: {r['Documento_identidad']} | Correo: {r['correo']} | Teléfono: {r['Telefono']}")
    except Error as e:
        print(f"Error al listar clientes: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def modificar_cliente():
    """Permite modificar los datos de un cliente existente por DNI."""
    cfg = get_mysql_config()
    conn = None
    try:
        conn = mysql.connector.connect(**cfg)
        cursor = conn.cursor()
        print("\n--- MODIFICAR CLIENTE ---")
        dni_a_modificar = input("DNI del cliente a modificar: ").strip()

        # Seleccionamos todas las columnas que podríamos querer modificar o mostrar
        cursor.execute("SELECT Nombre, Apellido, razon_social, correo, Telefono FROM clientes WHERE Documento_identidad = %s", (dni_a_modificar,))
        row = cursor.fetchone()
        
        if not row:
            print(f"No existe cliente con DNI {dni_a_modificar}.")
            return

        # Desempaquetamos los valores actuales
        actual_nombre, actual_apellido, actual_razon_social, actual_correo, actual_telefono = row
        
        print("Dejar en blanco para conservar el valor actual.")
        nuevo_nombre        = input(f"Nuevo Nombre ({actual_nombre}): ").strip() or actual_nombre
        nuevo_apellido      = input(f"Nuevo Apellido ({actual_apellido}): ").strip() or actual_apellido
        nueva_razon_social  = input(f"Nueva Razón social ({actual_razon_social}): ").strip() or actual_razon_social
        nuevo_correo        = input(f"Nuevo Correo ({actual_correo}): ").strip() or actual_correo
        nuevo_telefono_str  = input(f"Nuevo Teléfono ({actual_telefono}): ").strip() # Leer como string

        # Validación y conversión del nuevo teléfono
        if nuevo_telefono_str: # Si el usuario ingresó algo
            if not nuevo_telefono_str.isdigit():
                print("Error: El teléfono debe contener solo dígitos. No se modificará el teléfono.")
                nuevo_telefono = actual_telefono # Mantiene el valor actual si hay un error
            else:
                nuevo_telefono = int(nuevo_telefono_str)
        else:
            nuevo_telefono = actual_telefono # Conserva el valor actual si se dejó en blanco

        update_sql = """
            UPDATE clientes 
            SET Nombre = %s, Apellido = %s, razon_social = %s, correo = %s, Telefono = %s 
            WHERE Documento_identidad = %s
        """
        # Asegúrate de que el orden de los parámetros coincida con el UPDATE
        cursor.execute(update_sql, (nuevo_nombre, nuevo_apellido, nueva_razon_social, nuevo_correo, nuevo_telefono, dni_a_modificar))
        conn.commit()
        print(f"Cliente con DNI {dni_a_modificar} modificado correctamente.")
    except Error as e:
        print(f"Error al modificar cliente: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def eliminar_cliente():
    """Permite eliminar un cliente de la tabla por DNI."""
    cfg = get_mysql_config()
    conn = None
    try:
        conn = mysql.connector.connect(**cfg)
        cursor = conn.cursor()
        print("\n--- ELIMINAR CLIENTE ---")
        dni_a_eliminar = input("DNI del cliente a eliminar: ").strip() # Cambiado de cuit a dni

        cursor.execute("SELECT razon_social FROM clientes WHERE Documento_identidad = %s", (dni_a_eliminar,)) # Columna correcta
        row = cursor.fetchone()
        
        if not row:
            print(f"No existe cliente con DNI {dni_a_eliminar}.")
            return

        razon_social = row[0]
        confirm = input(f"¿Confirma eliminar a {razon_social} (S/N)? ").strip().upper()
        if confirm == 'S':
            cursor.execute("DELETE FROM clientes WHERE Documento_identidad = %s", (dni_a_eliminar,)) # Columna correcta
            conn.commit()
            print(f"Cliente {razon_social} eliminado correctamente.")
        else:
            print("Eliminación cancelada.")
    except Error as e:
        print(f"Error al eliminar cliente: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Al importar este módulo, aseguramos que la tabla exista
init_db()
