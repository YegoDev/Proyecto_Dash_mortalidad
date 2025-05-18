from dash import Dash
from carga_datos import cargar_datos, transformar_datos
from layout import generar_layout
from callbacks import registrar_callbacks

df_hechos, df_causa, df_loc = cargar_datos()
df = transformar_datos(df_hechos, df_causa, df_loc)

app = Dash(__name__)
server = app.server

app.layout = generar_layout()
registrar_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True)