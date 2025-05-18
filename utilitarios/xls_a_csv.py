import pandas as pd

# Hechos
df_hechos = pd.read_excel("data/Anexo1.NoFetal2019_CE_15-03-23.xlsx")
df_hechos.to_csv("data/Anexo1.NoFetal2019_CE_15-03-23.csv", index=False)

# Causa (omitimos cabecera decorativa)
df_causa = pd.read_excel("data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx", skiprows=8)
df_causa.columns = [
     'CAPITULO',
     'NOMBRE_CAPITULO',
     'CODIGO_CIE10_3C',
     'DESCRIPCION_CIE_3C',
     'CODIGO_CIE10_4C',
     'DESCRIPCION_CIE_4C'
]
df_causa.to_csv("data/Anexo2.CodigosDeMuerte_CE_15-03-23.csv", index=False)

# Locación
df_loc = pd.read_excel("data/Anexo3.Divipola_CE_15-03-23.xlsx")
df_loc.to_csv("data/Anexo3.Divipola_CE_15-03-23.csv", index=False)

print("✅ Archivos convertidos correctamente a CSV.")