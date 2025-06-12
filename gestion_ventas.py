import json
import os
import sqlite3
from datetime import datetime, timedelta

# JSON storage settings
DATA_FILE = 'ventas.json'

# SQLite DB settings
db_path = 'ventas.db'

# ---------- JSON-BASED FUNCTIONS ----------
def load_sales_json():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_sales_json(ventas):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(ventas, f, indent=4, ensure_ascii=False)


def register_sale(cliente, destino, fecha_str, costo):
    """Registra una venta en JSON (sin ventana de arrepentimiento)."""
    try:
        datetime.fromisoformat(fecha_str)
    except ValueError:
        print("Formato de fecha inválido.")
        return
    ventas = load_sales_json()
    ventas.append({
        'cliente': cliente,
        'destino': destino,
        'fecha': fecha_str,
        'costo': costo,
        'estado': 'Activa'
    })
    save_sales_json(ventas)
    print("✅ Venta registrada (JSON).")


def list_sales():
    """Lista ventas desde JSON."""
    ventas = load_sales_json()
    if not ventas:
        print("No hay ventas.")
        return
    for i, v in enumerate(ventas, 1):
        print(f"{i}. {v['cliente']} -> {v['destino']} | {v['fecha']} | {v['costo']} | {v['estado']}")

# ---------- SQLITE-BASED FUNCTIONS ----------
def init_db(db= db_path):
    """Inicializa la tabla SQLite para ventas con campo de anulación."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL,
        destino TEXT NOT NULL,
        monto REAL NOT NULL,
        fecha_registro TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'Activa',
        fecha_hora_anulacion TEXT
    )
    """)
    conn.commit()
    conn.close()


def register_sale_db(cliente, destino, monto, db=db_path):
    """Registra una venta en SQLite (se ignora fecha_str)."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    fecha_registro = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO ventas (cliente, destino, monto, fecha_registro) VALUES (?, ?, ?, ?)",
        (cliente, destino, monto, fecha_registro)
    )
    conn.commit()
    conn.close()
    print(f"✅ Venta registrada (DB): {cliente}->{destino} | {monto} | {fecha_registro}")


def list_sales_db(db= db_path):
    """Lista ventas desde SQLite."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT id, cliente, destino, monto, fecha_registro, estado FROM ventas")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print("No hay ventas en DB.")
        return
    for id_, c, d, m, f, e in rows:
        print(f"{id_}. {c}->{d} | {f} | {m} | {e}")


def annul_sale(sale_id, scale_minutes=5, db=db_path):
    """Anula venta en SQLite si está dentro de ventana de arrepentimiento."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT estado, fecha_registro FROM ventas WHERE id = ?", (sale_id,))
    row = cursor.fetchone()
    if not row:
        print(f"❌ Venta con ID {sale_id} no encontrada.")
        conn.close(); return
    estado_actual, fecha_registro_str = row
    if estado_actual == 'Anulada':
        print(f"⚠️ Venta {sale_id} ya anulada."); conn.close(); return
    fecha_reg = datetime.fromisoformat(fecha_registro_str)
    ahora = datetime.now()
    if ahora - fecha_reg > timedelta(minutes=scale_minutes):
        print(f"⚠️ Ventana de arrepentimiento vencida (> {scale_minutes} min)."); conn.close(); return
    fecha_anu = ahora.isoformat()
    cursor.execute(
        "UPDATE ventas SET estado='Anulada', fecha_hora_anulacion=? WHERE id=?",
        (fecha_anu, sale_id)
    )
    conn.commit()
    conn.close()
    print(f"✅ Venta {sale_id} anulada a las {fecha_anu}.")