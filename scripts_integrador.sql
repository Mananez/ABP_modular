-- scripts_integrador2.sql
-- DDL: Creación de tablas según el modelo relacional

-- 1. Tabla clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,         -- Identificador único
    nombre VARCHAR(100) NOT NULL,              -- Nombre del cliente
    email VARCHAR(150) UNIQUE NOT NULL         -- Email del cliente
);

-- 2. Tabla destinos
CREATE TABLE IF NOT EXISTS destinos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudad VARCHAR(100) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    costo_base DECIMAL(10,2) NOT NULL
);

-- 3. Tabla ventas
CREATE TABLE IF NOT EXISTS ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    destino_id INT NOT NULL,
    fecha_registro DATETIME NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    estado ENUM('Activa','Anulada') NOT NULL DEFAULT 'Activa',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (destino_id) REFERENCES destinos(id)
);

-- DML: Insertar datos de ejemplo (al menos 3 por tabla)

-- Clientes
INSERT INTO clientes (nombre, email) VALUES
('Ana Gómez',    'ana.gomez@ejemplo.com'),
('Luis Martínez','luis.martinez@ejemplo.com'),
('María Pérez',  'maria.perez@ejemplo.com');

-- Destinos
INSERT INTO destinos (ciudad, pais, costo_base) VALUES
('Roma',     'Italia',    1500.00),
('Sídney',   'Australia', 2500.00),
('Salta',    'Argentina',  800.00);

-- Ventas
INSERT INTO ventas (cliente_id, destino_id, fecha_registro, monto) VALUES
(1, 1, '2025-06-01 10:15:00', 1600.00),
(2, 3, '2025-06-02 14:30:00',  820.00),
(3, 2, '2025-06-03 09:45:00', 2550.00);

-- Consultas SELECT relevantes

-- 1) Listar todos los clientes
SELECT * FROM clientes;

-- 2) Mostrar las ventas realizadas en una fecha específica
-- (ej. 2025-06-02)
SELECT v.id, c.nombre, d.ciudad, v.fecha_registro, v.monto
FROM ventas v
JOIN clientes c ON v.cliente_id = c.id
JOIN destinos d ON v.destino_id = d.id
WHERE DATE(v.fecha_registro) = '2025-06-02';

-- 3) Obtener la última venta de cada cliente y su fecha
SELECT
  c.id AS cliente_id,
  c.nombre,
  MAX(v.fecha_registro) AS ultima_venta
FROM ventas v
JOIN clientes c ON v.cliente_id = c.id
GROUP BY c.id, c.nombre;

-- 4) Listar todos los destinos que empiezan con “S”
SELECT * FROM destinos
WHERE ciudad LIKE 'S%';

-- 5) Mostrar cuántas ventas se realizaron por país
SELECT
  d.pais,
  COUNT(*) AS total_ventas
FROM ventas v
JOIN destinos d ON v.destino_id = d.id
GROUP BY d.pais;
