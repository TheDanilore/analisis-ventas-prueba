-- consulta.sql
-- Consulta para obtener los 3 productos más vendidos por cantidad
-- Se ejecuta sobre la tabla 'ventas_limpias' creada por el script de Python.

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