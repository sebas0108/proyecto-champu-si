"""Sistema de Información Comercial - Distribuidora Capilaria S.A.S."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import solara

import datos

ORGANIZACION = "Distribuidora Capilaria S.A.S. — Línea Capilar"
NECESIDAD = "Monitorear las ventas mensuales de champú frente a la meta (250 uds) para decidir compras de inventario o promociones"
QUIEN_DECIDE = "Gerencia Comercial"
COMPONENTES = {
    "hardware": "Equipos cliente y el servidor gratuito en la nube (Render) donde corre la app",
    "software": "Esta app (Solara), datos.py, Matplotlib y SQLite",
    "datos": "Maestro de productos y serie histórica mensual de ventas de champú (1995–1997)",
    "personas": "Analista de ventas que registra datos y Gerente Comercial que toma decisiones",
    "tic": "Internet, GitHub y el navegador web por donde se consulta el tablero",
}
META_MENSUAL = 250.0

conn = datos.conectar()
anio = solara.reactive(1997)
nuevo = {c: solara.reactive("") for c in ["id_producto", "anio", "mes", "ventas"]}
mensaje = solara.reactive("")
recargar = solara.reactive(0)


def procesar(valores):
    """Valida antes de la base y registra. Devuelve un mensaje para la pantalla."""
    if any(str(x).strip() == "" for x in valores.values()):
        return "Rechazado: hay campos vacíos"
    try:
        prod = int(valores["id_producto"])
        anio_val = int(valores["anio"])
        ventas_val = float(valores["ventas"])
    except ValueError:
        return "Rechazado: id_producto y año deben ser enteros, y ventas un número"
    ok = datos.registrar(conn, prod, anio_val, valores["mes"].strip(), ventas_val)
    if ok:
        recargar.set(recargar.value + 1)
        anio.set(anio_val)
        return "Registrado correctamente"
    return "Rechazado por la base (producto inexistente, mes inválido o ventas negativas)"


@solara.component
def Page():
    _ = recargar.value
    solara.Title(ORGANIZACION)
    solara.Markdown(f"# {ORGANIZACION}\n\n**Para qué sirve:** {NECESIDAD}. **Quién decide:** {QUIEN_DECIDE}.")
    solara.Markdown("\n".join(f"- **{k}:** {v}" for k, v in COMPONENTES.items()))

    lista_anios = datos.anios_disponibles(conn)
    if anio.value not in lista_anios and lista_anios:
        anio.set(lista_anios[-1])

    with solara.Columns([1, 1]):
        with solara.Card("Consulta Operativa (TPS)"):
            solara.Select(label="Año", value=anio, values=lista_anios)
            filas = datos.consultar(conn, anio.value)
            df_mes = pd.DataFrame(filas, columns=["Código", "Producto", "Mes", "Ventas"])
            if len(df_mes):
                prom = round(df_mes["Ventas"].mean(), 1)
                if prom < META_MENSUAL:
                    solara.Warning(f"ALERTA DSS ({anio.value}): Promedio mensual de {prom} uds está por DEBAJO de la meta ({META_MENSUAL}). Activar promoción.")
                else:
                    solara.Success(f"META CUMPLIDA DSS ({anio.value}): Promedio mensual de {prom} uds SUPERA la meta ({META_MENSUAL}). Mantener inventario.")
            solara.DataFrame(df_mes)

        with solara.Card("Reporte Histórico Consolidado (MIS)"):
            tabla = pd.DataFrame(datos.reportar(conn),
                                 columns=["Año", "Producto", "Meses", "Total Ventas", "Promedio Mensual"])
            if len(tabla):
                fig, ax = plt.subplots(figsize=(5, 2.5))
                ax.bar(tabla["Año"].astype(str), tabla["Promedio Mensual"], color="#2a6fdb")
                ax.axhline(META_MENSUAL, color="red", linestyle="--", label="Meta (250)")
                ax.set_ylabel("Promedio mensual (uds)")
                ax.legend()
                ax.spines[["top", "right"]].set_visible(False)
                solara.FigureMatplotlib(fig)
                plt.close(fig)
            solara.DataFrame(tabla)

    with solara.Card("Registrar una venta mensual (TPS)"):
        solara.Markdown("_Ingrese: `id_producto` (1), `anio` (ej. 1998), `mes` (Jan..Dec), `ventas` (ej. 520.5)_")
        for nombre, estado in nuevo.items():
            solara.InputText(nombre, value=estado)

        def guardar():
            mensaje.set(procesar({k: e.value for k, e in nuevo.items()}))

        solara.Button("Guardar", on_click=guardar, color="primary")
        solara.Markdown(mensaje.value)

    solara.Markdown("_Datos históricos abiertos (Shampoo Sales). La app no guarda datos personales (Ley 1581 de 2012). "
                    "Lo registrado se pierde cuando el servidor gratuito reinicia._")