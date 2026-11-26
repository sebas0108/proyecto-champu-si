# Sistema de Información Comercial - Distribuidora Capilaria S.A.S.

## 1. Enlaces del Proyecto
* **Dirección pública de la aplicación:** https://tu-app.onrender.com *(actualizar tras desplegar en Render)*
* **Repositorio público en GitHub:** https://github.com/tu-usuario/proyecto_champu *(actualizar tras subir a GitHub)*

## 2. Identidad del Sistema de Información
* **Organización:** Distribuidora Capilaria S.A.S. (comercializadora de productos de cuidado personal).
* **Necesidad y quién decide:** La Gerencia Comercial requiere monitorear las ventas mensuales de la línea capilar frente a una meta mínima de 250 unidades/mes para decidir oportunamente sobre compras de inventario o campañas promocionales.
* **Cinco componentes del SI:**
  * **Hardware:** Servidor en la nube (Render) que aloja la aplicación y computadores/dispositivos cliente desde donde se consulta el tablero.
  * **Software:** Lenguaje Python, framework web Solara, librería gráfica Plotly y motor de base de datos SQLite.
  * **Datos:** Registros históricos mensuales de ventas de champú (1995–1997) y maestro de productos con sus metas mensuales.
  * **Personas:** Gerente Comercial (toma decisiones con base en el tablero y alertas) y Analista de Ventas (registra las nuevas transacciones mensuales).
  * **TIC:** Red Internet, protocolo HTTP/HTTPS y plataforma GitHub para control de versiones y despliegue continuo.

## 3. Proceso de Negocio y Tipo de SI
* **Proceso de negocio apoyado (Gestión y Control de Ventas Mensuales):**
  1. Consolidación de las unidades vendidas al cierre de cada mes.
  2. Validación e ingreso de la transacción en el módulo de registro del sistema.
  3. Actualización automática de los indicadores acumulados y promedios anuales.
  4. Evaluación del promedio mensual frente al umbral meta (250 unidades) para definir acciones comerciales o de abastecimiento.
* **Tipo de SI y justificación:** Es un sistema híbrido que integra tres niveles:
  * **TPS (Sistema de Procesamiento de Transacciones):** Captura, valida y almacena cada nuevo registro de venta mensual en la base de datos.
  * **MIS (Sistema de Información Gerencial):** Transforma los datos históricos en reportes consolidados (agrupados por año), tablas y gráficos comparativos.
  * **DSS (Sistema de Apoyo a la Decisión):** Evalúa una regla de umbral (meta de 250 unidades) y emite alertas automáticas con recomendaciones de acción para la gerencia.

## 4. Fuente de los Datos
Los datos históricos cargados en `semilla.sql` corresponden al conjunto de datos clásico **Shampoo Sales** (ventas mensuales de champú durante 3 años, 36 observaciones entre enero de 1995 y diciembre de 1997), publicado originalmente por Makridakis, Wheelwright & Hyndman (1998) y ampliamente utilizado como dataset abierto de referencia para análisis de series temporales. Consultado y cargado el 26 de noviembre de 2026.

## 5. Protección de Datos Personales (Ley 1581 de 2012)
Este sistema de información **no recolecta, procesa ni almacena datos personales** de clientes, proveedores ni empleados (tales como nombres, cédulas, teléfonos, correos electrónicos o direcciones). Toda la información registrada corresponde exclusivamente a códigos internos de producto (`SH-001`) y cifras agregadas de ventas mensuales, dando pleno cumplimiento al principio de minimización y finalidad establecido en la Ley 1581 de 2012 (Régimen General de Protección de Datos Personales en Colombia).

## 6. Cómo ejecutar el proyecto localmente
1. Clonar o descargar este repositorio y ubicarse en la carpeta del proyecto.
2. Instalar las dependencias ejecutando: `pip install -r requirements.txt`
3. Iniciar la aplicación web con: `solara run app.py`
4. Abrir en el navegador la dirección local indicada en consola (por defecto `http://localhost:8765`).

## 7. Uso de IA
Para el desarrollo de este proyecto se utilizó un asistente de inteligencia artificial (Gemini) como herramienta de apoyo para estructurar el esquema relacional en SQLite (`esquema.sql` y `semilla.sql`), parametrizar las consultas SQL en Python (`datos.py`), construir los componentes visuales del tablero en Solara (`app.py`) y redactar la documentación técnica del presente `README.md`.