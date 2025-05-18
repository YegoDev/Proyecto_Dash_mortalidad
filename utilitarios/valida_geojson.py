import pandas as pd
import json

# Cargar DataFrame
df = pd.read_csv("data/Anexo3.Divipola_CE_15-03-23.csv", dtype=str)
df["COD_DEPARTAMENTO"] = df["COD_DEPARTAMENTO"].str.zfill(2).str.strip()

# Cargar GeoJSON
with open("data/Colombia_geojson.json", encoding="utf-8") as f:
    geojson = json.load(f)

# Normalizar DPTO en el GeoJSON
for f in geojson["features"]:
    f["properties"]["DPTO"] = str(f["properties"]["DPTO"]).zfill(2).strip()

# Obtener conjuntos únicos
df_codigos = set(df["COD_DEPARTAMENTO"].dropna().unique())
geojson_codigos = set(f["properties"]["DPTO"] for f in geojson["features"])

# Comparar
no_en_geojson = df_codigos - geojson_codigos
no_en_df = geojson_codigos - df_codigos

print("Códigos del DataFrame que NO están en el GeoJSON:")
for cod in sorted(no_en_geojson):
    print(" -", cod)

print("\nCódigos del GeoJSON que NO están en el DataFrame:")
for cod in sorted(no_en_df):
    print(" -", cod)