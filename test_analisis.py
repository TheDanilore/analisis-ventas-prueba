"""
Script de pruebas para analisis_ventas.py

Ejecución (desde la terminal):
    pytest
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from analisis_ventas import calcular_total # Importamos la función a probar

@pytest.fixture
def datos_de_prueba():
    """Crea un DataFrame de ejemplo para usar en las pruebas."""
    data = {
        'producto': ['A', 'B'],
        'cantidad': [10, 5],
        'precio_unitario': [100, 20]
    }
    return pd.DataFrame(data)

def test_calcular_total(datos_de_prueba):
    """
    Valida que la columna 'total' se calcule correctamente.
    """
    # Llama a la función que queremos probar
    df_resultado = calcular_total(datos_de_prueba)
    
    # Define el resultado que esperamos
    data_esperada = {
        'producto': ['A', 'B'],
        'cantidad': [10, 5],
        'precio_unitario': [100, 20],
        'total': [1000, 100]  # 10*100=1000, 5*20=100
    }
    df_esperado = pd.DataFrame(data_esperada)
    
    # Compara si el DataFrame resultado es igual al esperado
    assert_frame_equal(df_resultado, df_esperado)

def test_calcular_total_vacio():
    """Valida que maneje un DataFrame vacío."""
    df_vacio = pd.DataFrame(columns=['cantidad', 'precio_unitario'])
    df_resultado = calcular_total(df_vacio)
    df_esperado = pd.DataFrame(columns=['cantidad', 'precio_unitario', 'total'])
    assert_frame_equal(df_resultado, df_esperado)