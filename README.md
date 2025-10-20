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

<img width="1000" height="600" alt="grafico" src="https://github.com/user-attachments/assets/4d45046f-d609-4ce9-89e6-3ccb5e9f3e1f" />


## 3. Ejecutar las Pruebas

Para validar que la función de cálculo de totales funciona correctamente, corre `pytest` desde tu terminal en la carpeta del proyecto:

```bash
pytest
```

Verás una salida que indica si las pruebas pasaron (`PASSED`).

<img width="1460" height="253" alt="Captura de pantalla 2025-10-20 151935" src="https://github.com/user-attachments/assets/7cb51aa4-f927-4f00-abd0-f578ae3a2b54" />


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

<img width="863" height="432" alt="Captura de pantalla 2025-10-20 152242" src="https://github.com/user-attachments/assets/84e31b1c-7334-4e61-b6fc-7fe70cbd7684" />
