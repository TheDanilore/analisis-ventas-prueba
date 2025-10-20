# Análisis de Ventas

Este proyecto carga un archivo `ventas.csv`, lo limpia, realiza un análisis de ventas básico, guarda los resultados en una base de datos SQLite y genera un gráfico de la facturación mensual.

## Estructura de Archivos

```
analisis-ventas-prueba/
├── analisis_ventas.py     # Script principal
├── test_analisis.py       # Pruebas con pytest
├── ventas.csv             # Datos de entrada
├── consulta.sql           # Consulta de ejemplo
├── requirements.txt       # Dependencias
├── README.md              # Este archivo
├── ventas.db              # (Generado por el script) Base de datos
└── grafico.png            # (Generado por el script) Gráfico de facturación
```

## 1. Instalación

Primero, debes instalar las dependencias necesarias:

```bash
# Se recomienda crear un entorno virtual primero
# python -m venv venv
# source venv/bin/activate (Para macOS y Linux) (en Windows: venv\Scripts\activate)

pip install -r requirements.txt
```

## 2. Ejecutar el Análisis Principal

Para correr el script completo (limpieza, análisis, creación de BD y gráfico), ejecuta:

```bash
python analisis_ventas.py
```

Esto imprimirá los resultados del análisis en la terminal y generará los archivos `ventas.db` y `grafico.png`.

## 3. Ejecutar las Pruebas

Para validar que la función de cálculo de totales funciona correctamente, corre `pytest` desde tu terminal en la carpeta del proyecto:

```bash
pytest
```

Verás una salida que indica si las pruebas pasaron (`PASSED`).

## 4. Consultar la Base de Datos

Puedes usar cualquier cliente de SQLite (como DB Browser for SQLite o uno integrado en tu editor de código) para abrir el archivo `ventas.db` que se generó.

Para obtener los 3 productos más vendidos por cantidad (como se pide en el ejercicio), puedes ejecutar el contenido del archivo `consulta.sql`:

```sql
SELECT
    producto,
    SUM(cantidad) AS cantidad_total
FROM
    ventas_limpias
GROUP BY
    producto
ORDER BY
    cantidad_total DESC
LIMIT 3;
```