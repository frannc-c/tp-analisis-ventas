import os
import pandas as pd
import matplotlib.pyplot as plt

# Ruta del archivo CSV dentro del proyecto
CSV_PATH = os.path.join("datos", "ventas.csv")

# Ruta de salida del gráfico
GRAPH_PATH = os.path.join("resultados", "evolucion_ventas.png")

# Verificamos que el archivo exista
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"No se encontró el archivo: {CSV_PATH}")

# Leemos el CSV
df = pd.read_csv(CSV_PATH)

# Comentario técnico:
# Convertimos la columna de fecha a formato datetime para poder
# ordenar correctamente la serie temporal.
df["sales_date"] = pd.to_datetime(df["sales_date"], errors="coerce")

# Convertimos el monto de ventas a numérico para poder sumar y graficar.
df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce")

# Eliminamos filas con datos inválidos
df = df.dropna(subset=["sales_date", "sales_amount"])

# Agrupamos por fecha porque la consigna pide representar
# la evolución de las ventas en el tiempo.
ventas_por_dia = (
    df.groupby("sales_date", as_index=False)["sales_amount"]
    .sum()
    .sort_values("sales_date")
)

# Creamos la carpeta resultados si no existe
os.makedirs("resultados", exist_ok=True)

# Generamos el gráfico de línea
plt.figure(figsize=(10, 5))
plt.plot(
    ventas_por_dia["sales_date"],
    ventas_por_dia["sales_amount"],
    marker="o"
)

# El gráfico de líneas es el más adecuado para mostrar evolución temporal.
plt.title("Evolución de las ventas")
plt.xlabel("Fecha")
plt.ylabel("Monto de ventas")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Guardamos la imagen en la carpeta resultados
plt.savefig(GRAPH_PATH)
plt.close()

print("Gráfico generado correctamente.")
print(f"Archivo guardado en: {GRAPH_PATH}")
