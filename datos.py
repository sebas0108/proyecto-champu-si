"""Capa de datos: funciones con parámetros ?, sin pantallas."""
import sqlite3
from pathlib import Path

CARPETA = Path(__file__).parent
RUTA_BD = CARPETA / "base.db"


def conectar():
    """Abre la base; si no existe, la crea desde esquema.sql y semilla.sql."""
    nueva = not RUTA_BD.exists()
    conn = sqlite3.connect(RUTA_BD, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    if nueva:
        conn.executescript((CARPETA / "esquema.sql").read_text(encoding="utf-8"))
        conn.executescript((CARPETA / "semilla.sql").read_text(encoding="utf-8"))
        conn.commit()
    return conn


def anios_disponibles(conn):
    """Lista de años registrados para el selector."""
    return [a for (a,) in conn.execute("SELECT DISTINCT anio FROM ventas_mensuales ORDER BY anio")]


def consultar(conn, anio):
    """Consulta operativa (TPS): ventas mensuales de un año."""
    sql = """SELECT p.codigo, p.nombre, v.mes, v.ventas
             FROM ventas_mensuales v JOIN productos p ON p.id_producto = v.id_producto
             WHERE v.anio = ? ORDER BY v.id_venta"""
    return conn.execute(sql, (anio,)).fetchall()


def reportar(conn):
    """Reporte (MIS): total y promedio mensual por año y producto."""
    sql = """SELECT v.anio, p.nombre, COUNT(*) AS meses,
                    ROUND(SUM(v.ventas), 1) AS total_ventas,
                    ROUND(AVG(v.ventas), 1) AS promedio_mensual
             FROM ventas_mensuales v JOIN productos p ON p.id_producto = v.id_producto
             GROUP BY v.anio, p.nombre ORDER BY v.anio ASC"""
    return conn.execute(sql).fetchall()


def registrar(conn, id_producto, anio, mes, ventas):
    """Registro (TPS): guarda una venta mensual; si la base la rechaza, devuelve False."""
    sql = """INSERT INTO ventas_mensuales (id_producto, anio, mes, ventas) VALUES (?, ?, ?, ?)"""
    try:
        conn.execute(sql, (id_producto, anio, mes, ventas))
        conn.commit()
        return True
    except sqlite3.IntegrityError as error:
        conn.rollback()
        print("Rechazado por la base:", error)
        return False