# SkyRoute

**Sistema de Gestión de Pasajes y Vuelos**

SkyRoute es una aplicación en Python que permite administrar clientes, destinos y ventas de pasajes a distintos vuelos, incluyendo la funcionalidad de cancelación (botón de arrepentimiento) para anular ventas recientes. Utiliza MySQL para la persistencia de datos y ofrece un menú de consola modularizado.

## Integrantes del Grupo 26

* Agustín Díaz - DNI: 42108462 - (https://github.com/TheBloodCold)
* Cristian Lizio - DNI: 27078187 - (https://github.com/cristianjl79)
* Mayco Ñañez - DNI: 38332846 - (https://github.com/Mananez)

## Estructura del Repositorio

```
skyroute/
├── config.py                # Configuración de conexión a MySQL
├── main.py                  # Menú principal y orquestación de módulos
├── conexion_base_datos.py   # Funciones para conectar y ejecutar consultas en MySQL
├── gestion_clientes.py      # CRUD de clientes en MySQL
├── gestion_destinos.py      # CRUD de destinos en MySQL
├── gestion_ventas.py        # Registro y anulación de ventas (JSON, SQLite y MySQL)
├── scripts_integrador.sql  # Sentencias DDL, DML y consultas SQL comentadas
└── requirements.txt         # Dependencias del proyecto
```

## Instrucciones de Ejecución

1. Clonar el repositorio y acceder al directorio:

   ```bash
   git clone https://github.com/tu-usuario/skyroute.git
   cd skyroute
   ```
2. (Opcional) Crear un entorno virtual e instalar dependencias:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```
3. Configurar las credenciales de MySQL en `config.py` o mediante variables de entorno:

   ```bash
   export MYSQL_HOST=localhost
   export MYSQL_USER=usuario
   export MYSQL_PASSWORD=contraseña
   export MYSQL_DB=skyroute
   ```
4. Iniciar la aplicación:

   ```bash
   python main.py
   ```
5. En el menú, seleccionar la opción deseada.

## Detalle de Archivos

* **config.py**: Parámetros de conexión a la base de datos.
* **conexion\_base\_datos.py**: Funciones `get_connection` y `execute_query` para interactuar con MySQL.
* **gestion\_clientes.py**: Funciones para crear, listar, modificar y eliminar clientes.
* **gestion\_destinos.py**: Funciones para crear, listar, modificar y eliminar destinos.
* **gestion\_ventas.py**: Registro y anulación de ventas usando JSON, SQLite y MySQL.
* **scripts\_integrador2.sql**: Archivo con sentencias SQL de creación de tablas (DDL), inserción de datos de ejemplo (DML) y consultas SELECT.
* **scripts\_creacion\_clientes.sql**: Script específico para crear la tabla `clientes`.
* **requirements.txt**: Listado de dependencias Python (e.g., mysql-connector-python).
