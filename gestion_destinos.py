import json
import os

DATA_FILE = 'destinos.json'

def load_destinations():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_destinations(destinos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(destinos, f, indent=4, ensure_ascii=False)

def register_destination(ciudad, pais, costo_base):
    destinos = load_destinations()
    if any(d['ciudad'].lower()==ciudad.lower() and d['pais'].lower()==pais.lower() for d in destinos):
        print(f"El destino {ciudad}, {pais} ya existe.")
        return
    destinos.append({'ciudad': ciudad, 'pais': pais, 'costo_base': costo_base})
    save_destinations(destinos)
    print(f"Destino {ciudad}, {pais} agregado.")

def list_destinations():
    destinos = load_destinations()
    if not destinos:
        print("No hay destinos registrados.")
        return
    for i, d in enumerate(destinos, 1):
        print(f"{i}. {d['ciudad']} ({d['pais']}) - Costo: {d['costo_base']}")

def modify_destination(index, ciudad, pais, costo_base):
    destinos = load_destinations()
    if index<1 or index>len(destinos):
        print("Índice inválido.")
        return
    destinos[index-1] = {'ciudad': ciudad, 'pais': pais, 'costo_base': costo_base}
    save_destinations(destinos)
    print(f"Destino {index} modificado.")

def delete_destination(index):
    destinos = load_destinations()
    if index<1 or index>len(destinos):
        print("Índice inválido.")
        return
    eliminado = destinos.pop(index-1)
    save_destinations(destinos)
    print(f"Destino {eliminado['ciudad']}, {eliminado['pais']} eliminado.")
