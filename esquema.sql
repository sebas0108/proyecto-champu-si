CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    linea TEXT NOT NULL CHECK (linea IN ('Capilar', 'Corporal', 'Facial')),
    meta_mensual REAL NOT NULL CHECK (meta_mensual > 0)
);

CREATE TABLE IF NOT EXISTS ventas_mensuales (
    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL,
    anio INTEGER NOT NULL CHECK (anio >= 1990),
    mes TEXT NOT NULL CHECK (mes IN ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')),
    ventas REAL NOT NULL CHECK (ventas >= 0),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);