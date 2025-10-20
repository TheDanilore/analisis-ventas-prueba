"""
Script principal para el Análisis de Ventas.

Ejecución:
    python analisis_ventas.py
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import os
import sys

def cargar_limpiar_datos(filepath="ventas.csv"):
    """
    Carga los datos desde un CSV, los limpia y convierte tipos.
    """
    if not os.path.exists(filepath):
        print(f"Error: El archivo {filepath} no se encuentra.", file=sys.stderr)
        return pd.DataFrame() # Retorna un DataFrame vacío

    try:
        df = pd.read_csv(filepath)
        
        # 1. Corregir error tipográfico común en los datos de ejemplo
        if '2E-05-25' in df['fecha'].values:
            df['fecha'] = df['fecha'].replace('2E-05-25', '2023-05-25')
            
        # 2. Limpieza de nulos
        df = df.dropna()
        
        # 3. Conversión de fecha
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # 4. Asegurar tipos de dato numéricos
        df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
        df['precio_unitario'] = pd.to_numeric(df['precio_unitario'], errors='coerce')

        # 5. Limpieza de inconsistentes (cantidad > 0 y nulos de coerción)
        df = df.dropna(subset=['cantidad', 'precio_unitario'])
        df = df[df['cantidad'] > 0].copy()
        
        return df
    
    except Exception as e:
        print(f"Error al cargar o limpiar datos: {e}", file=sys.stderr)
        return pd.DataFrame()

def calcular_total(df):
    """
    Añade la columna 'total' (cantidad * precio_unitario) a un DataFrame.
    Esta función es la que se probara con pytest.
    """
    if 'cantidad' in df.columns and 'precio_unitario' in df.columns:
        df['total'] = df['cantidad'] * df['precio_unitario']
        return df
    else:
        print("Error: Columnas 'cantidad' o 'precio_unitario' no encontradas.", file=sys.stderr)
        return df

def realizar_analisis(df):
    """
    Calcula el producto más vendido, el de mayor facturación y la facturación mensual.
    """
    if df.empty or 'total' not in df.columns:
        print("DataFrame vacío o sin columna 'total'. No se puede analizar.", file=sys.stderr)
        return None, None, pd.Series(dtype=float)

    # a) Producto más vendido por cantidad
    productos_por_cantidad = df.groupby('producto')['cantidad'].sum()
    producto_mas_vendido = productos_por_cantidad.idxmax()
    cantidad_maxima = productos_por_cantidad.max()

    # b) Producto con mayor facturación total
    productos_por_facturacion = df.groupby('producto')['total'].sum()
    producto_mayor_facturacion = productos_por_facturacion.idxmax()
    facturacion_maxima = productos_por_facturacion.max()

    # c) Facturación total por mes
    facturacion_mensual = df.groupby(df['fecha'].dt.to_period('M'))['total'].sum()
    facturacion_mensual.index.name = 'mes'

    # Imprimir resultados del análisis en la consola
    print("--- Resultados del Análisis ---")
    print(f"a) Producto más vendido por cantidad: {producto_mas_vendido} (Unidades: {cantidad_maxima})")
    print(f"b) Producto con mayor facturación: {producto_mayor_facturacion} (Total: ${facturacion_maxima:,.0f})")
    print("\nc) Facturación total por mes:")
    for mes, total in facturacion_mensual.sort_index().items():
        print(f"   {mes}: ${total:,.0f}")
    print("---------------------------------")
    
    return producto_mas_vendido, producto_mayor_facturacion, facturacion_mensual

def guardar_en_db(df, facturacion_mensual, db_path="ventas.db"):
    """
    Guarda los datos limpios y el análisis mensual en una base de datos SQLite.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            # Guardar tabla de ventas limpias (con 'total')
            df_db = df.copy()
            df_db['fecha'] = df_db['fecha'].astype(str) # Convertir fecha a texto para SQLite
            df_db.to_sql('ventas_limpias', conn, if_exists='replace', index=False)
            
            # Guardar análisis de facturación mensual
            df_fact_mensual = facturacion_mensual.reset_index()
            df_fact_mensual.columns = ['mes', 'facturacion_total']
            df_fact_mensual['mes'] = df_fact_mensual['mes'].astype(str) # Convertir Period a texto
            df_fact_mensual.to_sql('facturacion_mensual', conn, if_exists='replace', index=False)
            
        print(f"Datos guardados exitosamente en la base de datos: {db_path}")
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}", file=sys.stderr)

def generar_grafico(facturacion_mensual, img_path="grafico.png"):
    """
    Genera un gráfico de barras de la facturación mensual y lo guarda.
    """
    if facturacion_mensual.empty:
        print("No hay datos para graficar.", file=sys.stderr)
        return

    try:
        datos_grafico = facturacion_mensual.sort_index()
        x_labels = datos_grafico.index.to_timestamp() # Convertir PeriodIndex a Timestamps
        y_values = datos_grafico.values

        plt.figure(figsize=(10, 6))
        bars = plt.bar(x_labels, y_values, width=20, align='center', color='skyblue', edgecolor='black')

        # Formatear eje Y como moneda
        formatter = mticker.FuncFormatter(lambda x, p: f'${x:,.0f}')
        plt.gca().yaxis.set_major_formatter(formatter)

        # Formatear eje X para mostrar "Año-Mes"
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

        plt.title('Facturación Total por Mes', fontsize=16, fontweight='bold')
        plt.xlabel('Mes', fontsize=12)
        plt.ylabel('Facturación Total', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Añadir etiquetas de valor sobre las barras
        for bar in bars:
            height = bar.get_height()
            plt.gca().annotate(f'${height:,.0f}',
                               xy=(bar.get_x() + bar.get_width() / 2, height),
                               xytext=(0, 3),  # 3 puntos de offset vertical
                               textcoords="offset points",
                               ha='center', va='bottom', fontsize=9)

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(img_path)
        print(f"Gráfico guardado exitosamente como: {img_path}")
    except Exception as e:
        print(f"Error al generar el gráfico: {e}", file=sys.stderr)

def main():
    """
    Función principal que orquesta todo el proceso.
    """
    # 1. Carga y limpieza
    df_limpio = cargar_limpiar_datos(filepath="ventas.csv")
    if df_limpio.empty:
        print("No se pudieron cargar los datos. Terminando ejecución.", file=sys.stderr)
        return

    # 2. Cálculo de columna 'total'
    df_completo = calcular_total(df_limpio)

    # 3. Análisis
    _, _, fact_mes = realizar_analisis(df_completo)

    # 4. Persistencia en DB
    if not df_completo.empty and not fact_mes.empty:
        guardar_en_db(df_completo, fact_mes, db_path="ventas.db")
    else:
        print("No se generaron datos para guardar en la base de datos.", file=sys.stderr)

    # 5. Visualización
    if not fact_mes.empty:
        generar_grafico(fact_mes, img_path="grafico.png")
    else:
        print("No se generaron datos de facturación mensual para el gráfico.", file=sys.stderr)

if __name__ == "__main__":
    main()