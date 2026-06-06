import os
import pandas as pd

# Ruta del archivo CSV dentro del proyecto
CSV_PATH = os.path.join("datos", "ventas.csv")

# Ruta de salida del resumen
OUTPUT_PATH = os.path.join("resultados", "resumen_ventas.txt")

# Verificamos que el archivo exista
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"No se encontró el archivo: {CSV_PATH}")

# Leemos el CSV
df = pd.read_csv(CSV_PATH)

# Convertimos la columna de fecha a formato fecha para poder trabajar
# con orden temporal y agrupar las ventas por día o por mes.
df["sales_date"] = pd.to_datetime(df["sales_date"], errors="coerce")

# Convertimos el monto de ventas a numérico para evitar errores
# en los cálculos estadísticos.
df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce")

# Eliminamos filas inválidas o incompletas
df = df.dropna(subset=["sales_date", "sales_amount"])

# Indicadores básicos
ventas_totales = df["sales_amount"].sum()
venta_promedio = df["sales_amount"].mean()
venta_maxima = df["sales_amount"].max()
venta_minima = df["sales_amount"].min()

# Agrupamos por mes para resumir la evolución general de las ventas.
df["mes"] = df["sales_date"].dt.to_period("M").astype(str)
ventas_por_mes = df.groupby("mes")["sales_amount"].sum().reset_index()
ventas_por_mes = ventas_por_mes.sort_values("mes")

# Creamos la carpeta resultados si no existe
os.makedirs("resultados", exist_ok=True)

# Guardamos el resumen en un archivo de texto
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write("RESUMEN DEL ANÁLISIS DE VENTAS\n")
    f.write("=" * 40 + "\n\n")
    f.write(f"Ventas totales: ${ventas_totales:,.2f}\n")
    f.write(f"Venta promedio diaria: ${venta_promedio:,.2f}\n")
    f.write(f"Venta máxima diaria: ${venta_maxima:,.2f}\n")
    f.write(f"Venta mínima diaria: ${venta_minima:,.2f}\n\n")
    f.write("Ventas por mes:\n")
    f.write(ventas_por_mes.to_string(index=False))

print("Análisis completado correctamente.")
print(f"Resumen guardado en: {OUTPUT_PATH}")
