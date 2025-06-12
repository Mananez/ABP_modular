# main.py
import gestion_cliente as gc
import gestion_destinos as gd
import gestion_ventas as gv
import conexion_base_datos as db
from config import get_mysql_config
import os

SQL_SCRIPT = 'scripts_integrador2.sql'

def menu_principal():
    """Muestra el menú principal de SkyRoute."""
    print("="*46)
    print("##  ----- Bienvenidos a SkyRoute -------    ##")
    print("="*46)
    print("## 1. Gestión de Clientes                   ##")
    print("## 2. Gestión de Destinos                   ##")
    print("## 3. Gestión de Ventas                     ##")
    print("## 4. Acerca del Sistema                    ##")
    print("## 5. Operaciones Base de Datos MySQL       ##")
    print("## 6. Salir                                 ##")
    print("="*46)
    return input("Seleccione una opción: ").strip()


def gestionar_clientes():
    init = getattr(gc, 'init_db', None)
    if callable(init): init()
    while True:
        print("\n--- GESTIÓN DE CLIENTES ---")
        print("1. Listar clientes")
        print("2. Agregar cliente")
        print("3. Modificar cliente")
        print("4. Eliminar cliente")
        print("5. Volver")
        opc = input("Seleccione una opción: ").strip()
        if opc == '1':
            gc.listar_clientes()
        elif opc == '2':
            gc.agregar_cliente()
        elif opc == '3':
            gc.modificar_cliente()
        elif opc == '4':
            gc.eliminar_cliente()
        elif opc == '5':
            break
        else:
            print("Opción inválida. Intente nuevamente.")


def gestionar_destinos():
    init = getattr(gd, 'init_db', None)
    if callable(init): init()
    while True:
        print("\n--- GESTIÓN DE DESTINOS ---")
        print("1. Listar destinos")
        print("2. Agregar destino")
        print("3. Modificar destino")
        print("4. Eliminar destino")
        print("9. Volver")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == '1':
            gd.list_destinations()
        elif opcion == '2':
            ciudad = input("Ciudad: ").strip()
            pais   = input("País: ").strip()
            costo  = float(input("Costo base: "))
            gd.register_destination(ciudad, pais, costo)
        elif opcion == '3':
            gd.list_destinations()
            did   = int(input("ID a modificar: "))
            ciudad = input("Nueva ciudad: ").strip()
            pais   = input("Nuevo país: ").strip()
            costo  = float(input("Nuevo costo base: "))
            gd.modify_destination(did, ciudad, pais, costo)
        elif opcion == '4':
            gd.list_destinations()
            did = int(input("ID a eliminar: "))
            gd.delete_destination(did)
        elif opcion == '5':
            break
        else:
            print("Opción inválida. Intente nuevamente.")


def gestionar_ventas():
    init = getattr(gv, 'init_db', None)
    if callable(init): init()
    while True:
        print("\n--- GESTIÓN DE VENTAS ---")
        print("1. Listar ventas JSON")
        print("2. Registrar venta JSON")
        print("3. Anular venta JSON")
        print("4. Listar ventas SQLite")
        print("5. Registrar venta SQLite")
        print("6. Anular venta SQLite")
        print("7. Volver")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == '1': gv.list_sales()
        elif opcion == '2':
            c = input("Cliente: ").strip()
            d = input("Destino: ").strip()
            f = input("Fecha (YYYY-MM-DD): ").strip()
            m = float(input("Costo: "))
            gv.register_sale(c, d, f, m)
        elif opcion == '3':
            gv.list_sales()
            i = int(input("Índice a anular: "))
            gv.annul_sale(i)
        elif opcion == '4': gv.list_sales_db()
        elif opcion == '5':
            c = input("Cliente: ").strip()
            d = input("Destino: ").strip()
            m = float(input("Monto: "))
            gv.register_sale_db(c, d, m)
        elif opcion == '6':
            gv.list_sales_db()
            i = int(input("ID a anular: "))
            gv.annul_sale(i)
        elif opcion == '7': break
        else: print("Opción inválida.")


def acerca_del_sistema():
    print("\n--- ACERCA DEL SISTEMA ---")
    print("SkyRoute - Sistema de Gestión de Pasajes")
    print("Versión 1.0")
    print("Desarrollado por Grupo 26")


def gestionar_bd():
    cfg = get_mysql_config()
    print(f"\nConectando a MySQL en {cfg['host']}:{cfg['port']} DB={cfg['database']}")
    while True:
        print("\n--- BD MySQL ---")
        print("1. Crear DDL+DML inicial")
        print("2. Inserts adicionales")
        print("3. Consultas ejemplo")
        print("4. Volver")
        o = input("Opción: ").strip()
        if o=='1':
            if not os.path.exists(SQL_SCRIPT): print(f"No {SQL_SCRIPT}"); continue
            with open(SQL_SCRIPT,'r') as f: sql=f.read()
            db.execute_query(sql)
            print("Cargado inicial.")
        elif o=='2':
            ins="""
            INSERT INTO clientes (razon_social,cuit,correo) VALUES
            ('Pedro','20-12345678-9','p@e.com'),('Lucia','27-87654321-0','l@e.com'),('Marcos','23-11223344-5','m@e.com');
            INSERT INTO destinos (ciudad,pais,costo_base) VALUES
            ('Salzburgo','Austria',1200),('San Pablo','Brasil',900),('Seattle','EEUU',1600);
            INSERT INTO ventas (cliente_id,destino_id,fecha_registro,monto) VALUES
            (4,4,'2025-06-05 11:00:00',1250),(5,5,'2025-06-06 12:30:00',950),(6,6,'2025-06-07 09:15:00',1650);
            """
            db.execute_query(ins)
            print("Inserts ok.")
        elif o=='3':
            qs={"Listar clientes":"SELECT razon_social,cuit,correo FROM clientes;",
                "Ventas 02-06":"SELECT v.id,c.razon_social,d.ciudad,v.fecha_registro,v.monto FROM ventas v JOIN clientes c ON v.cliente_id=c.id JOIN destinos d ON v.destino_id=d.id WHERE DATE(v.fecha_registro)='2025-06-02';",
                "Ult venta cliente":"SELECT c.id,c.razon_social,MAX(v.fecha_registro) ultima FROM ventas v JOIN clientes c ON v.cliente_id=c.id GROUP BY c.id,c.razon_social;",
                "Destinos S":"SELECT ciudad,pais,costo_base FROM destinos WHERE ciudad LIKE 'S%';",
                "Ventas x pais":"SELECT d.pais,COUNT(*) total FROM ventas v JOIN destinos d ON v.destino_id=d.id GROUP BY d.pais;"}
            for t,q in qs.items(): print(f"\n-- {t} --"); rows=db.execute_query(q,fetch=True); [print(r) for r in rows]
        elif o=='4': break
        else: print("Inválido.")


def main():
    while True:
        op=menu_principal()
        if op=='1': gestionar_clientes()
        elif op=='2': gestionar_destinos()
        elif op=='3': gestionar_ventas()
        elif op=='4': acerca_del_sistema()
        elif op=='5': gestionar_bd()
        elif op=='9': print("\nGracias y hasta luego!"); break
        else: print("Inválida.")

if _name=="main_": main()